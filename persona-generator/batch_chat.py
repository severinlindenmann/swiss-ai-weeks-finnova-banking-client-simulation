import streamlit as st
import json
import os
from datetime import datetime
from llm import SwissAIClient
import glob
from dotenv import load_dotenv
import concurrent.futures
import time
from ui_components import load_custom_css, create_header, create_section_header, create_info_box, create_metric_card

# Load environment variables
load_dotenv()

def load_persona_batches():
    """Load all persona batches from JSON files"""
    batches = []
    
    # Check if generated_personas directory exists
    personas_dir = "generated_personas"
    if not os.path.exists(personas_dir):
        return []
    
    # Load persona batches
    for filename in glob.glob(os.path.join(personas_dir, "personas_batch_*.json")):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                batch_file = json.load(f)
                
                # Handle new format with metadata and personas array
                if isinstance(batch_file, dict) and 'personas' in batch_file:
                    metadata = batch_file.get('metadata', {})
                    personas_list = batch_file['personas']
                    
                    # Create batch info
                    batch_info = {
                        'filename': os.path.basename(filename),
                        'display_name': f"Batch {os.path.basename(filename).split('_')[-1].replace('.json', '')} ({len(personas_list)} Personas)",
                        'personas': personas_list,
                        'metadata': metadata,
                        'count': len(personas_list)
                    }
                    batches.append(batch_info)
                    
        except Exception as e:
            st.sidebar.warning(f"Could not load batch {filename}: {e}")
    
    return batches

def create_batch_persona_prompt(persona_data, user_question):
    """Create a system prompt for a persona to respond in a batch context"""
    
    persona = persona_data['persona']
    basic_info = persona.get('basic_info', {})
    demographics = persona.get('demographics', {})
    professional = persona.get('professional', {})
    financial = persona.get('financial', {})
    banking = persona.get('banking_persona', {})
    
    name = basic_info.get('name', 'Unknown')
    age = basic_info.get('age', 'Unknown')
    occupation = professional.get('job_title', 'Unknown')
    income = financial.get('disposable_income_category', 'Unknown')
    financial_exp = financial.get('financial_experience', 'Unknown')
    
    system_prompt = f"""Du bist {name}, {age} Jahre alt, {occupation} aus der Schweiz.

DEINE PROFILE:
- Einkommen: {income}
- Finanz-Erfahrung: {financial_exp}
- Deine vollständigen Daten: {json.dumps(persona, ensure_ascii=False)}

BATCH CHAT REGELN:
- Antworte als {name} in 1-2 kurzen Sätzen
- Fokussiere auf deine persönliche Meinung basierend auf deinem Profil
- Sei direkt und ehrlich
- Keine Grüße oder Höflichkeitsfloskeln

Frage: {user_question}
Antwort als {name}:"""

    return system_prompt

def get_batch_responses(selected_batch, user_question, api_key, max_personas=10):
    """Get responses from multiple personas in parallel"""
    
    if not user_question.strip():
        return []
    
    # Limit number of personas for performance
    personas_to_query = selected_batch['personas'][:max_personas]
    
    def get_single_response(persona_data):
        try:
            system_prompt = create_batch_persona_prompt(persona_data, user_question)
            client = SwissAIClient(api_key=api_key)
            
            response = client.complete(
                prompt=user_question,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=100  # Very short responses for batch
            )
            
            persona = persona_data['persona']
            basic_info = persona.get('basic_info', {})
            name = basic_info.get('name', 'Unknown')
            age = basic_info.get('age', 'Unknown')
            job = persona.get('professional', {}).get('job_title', 'Unknown')
            
            return {
                'name': name,
                'age': age,
                'job': job,
                'response': response,
                'success': True
            }
            
        except Exception as e:
            return {
                'name': 'Error',
                'age': 'N/A',
                'job': 'N/A',
                'response': f"Error: {str(e)}",
                'success': False
            }
    
    # Use ThreadPoolExecutor for parallel requests (limited to 3 to avoid rate limits)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Add small delays between submissions to respect rate limits
        futures = []
        for i, persona in enumerate(personas_to_query):
            if i > 0:
                time.sleep(0.3)  # 300ms delay between submissions
            future = executor.submit(get_single_response, persona)
            futures.append(future)
        
        # Collect results
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
    
    return results

def display_batch_responses(responses):
    """Display responses from multiple personas"""
    
    if not responses:
        st.warning("Keine Antworten erhalten.")
        return
    
    # Sort by success first, then by name
    responses.sort(key=lambda x: (not x['success'], x['name']))
    
    st.subheader(f"💬 {len(responses)} Persona Antworten")
    
    # Display successful responses
    successful_responses = [r for r in responses if r['success']]
    
    for i, response in enumerate(successful_responses):
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"**{response['name']}**")
                st.caption(f"{response['age']} J., {response['job']}")
            
            with col2:
                st.markdown(f"*\"{response['response']}\"*")
            
            if i < len(successful_responses) - 1:
                st.divider()
    
    # Show errors if any
    error_responses = [r for r in responses if not r['success']]
    if error_responses:
        st.error(f"❌ {len(error_responses)} Fehler aufgetreten")

def show_batch_summary(chat_history, selected_batch):
    """Show a summary of the batch chat conversation"""
    
    if not chat_history:
        st.info("Keine Chat-Daten vorhanden.")
        return
    
    st.subheader("📋 Chat Zusammenfassung")
    
    # Overview metrics
    total_questions = len(chat_history)
    total_responses = sum(len([r for r in item['responses'] if r['success']]) for item in chat_history)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fragen gestellt", total_questions)
    with col2:
        st.metric("Antworten erhalten", total_responses)
    with col3:
        st.metric("Personas befragt", selected_batch['count'])
    
    st.divider()
    
    # Question summary
    st.subheader("❓ Gestellte Fragen:")
    for i, chat_item in enumerate(chat_history, 1):
        successful_responses = [r for r in chat_item['responses'] if r['success']]
        st.write(f"**{i}.** {chat_item['question']}")
        st.write(f"└─ {len(successful_responses)} Antworten erhalten")
        
        # Show response sentiment/themes (simple analysis)
        if successful_responses:
            responses_text = " ".join([r['response'] for r in successful_responses])
            
            # Simple keyword analysis
            positive_words = ['ja', 'gut', 'interessant', 'wichtig', 'nützlich', 'toll']
            negative_words = ['nein', 'nicht', 'schlecht', 'unnötig', 'problematisch']
            
            positive_count = sum(1 for word in positive_words if word in responses_text.lower())
            negative_count = sum(1 for word in negative_words if word in responses_text.lower())
            
            if positive_count > negative_count:
                st.write(f"   📈 Tendenz: Eher positiv ({positive_count} positive Signale)")
            elif negative_count > positive_count:
                st.write(f"   📉 Tendenz: Eher negativ ({negative_count} negative Signale)")
            else:
                st.write(f"   ⚖️ Tendenz: Gemischt")
        
        st.write("")

def batch_chat_page():
    """Main batch chat page"""
    # Load custom CSS
    load_custom_css()
    
    create_header(
        "Batch Chat", 
        "Chat mit mehreren Personas gleichzeitig - ideal für Produktideen und Marktforschung!",
        "👥"
    )
    
    # Get API key from environment
    api_key = os.getenv("SWISS_AI_PLATFORM_API_KEY")
    
    if not api_key:
        create_info_box("""
        <strong>🔑 API Key erforderlich</strong><br>
        Bitte gib deinen Swiss AI Platform API Key ein, um zu starten.
        """, "warning")
        api_key = st.text_input("Swiss AI API Key", type="password", key="batch_chat_api_key", placeholder="Dein API Key hier eingeben...")
        if not api_key:
            return
    
    # Load batches
    batches = load_persona_batches()
    
    if not batches:
        create_info_box("""
        <strong>⚠️ Keine Persona-Batches gefunden!</strong><br>
        Generiere zuerst Batches mit der Batch Generation Seite.
        """, "warning")
        return
    
    # Batch selection
    create_section_header("Batch wählen", "📦")
    
    batch_options = {batch['display_name']: batch for batch in batches}
    
    selected_display_name = st.selectbox(
        "Batch:",
        list(batch_options.keys()),
        key="batch_selector"
    )
    
    if selected_display_name:
        selected_batch = batch_options[selected_display_name]
        
        # Show batch info
        col1, col2, col3 = st.columns(3)
        with col1:
            create_metric_card("Personas", selected_batch['count'], "👥")
        with col2:
            create_metric_card("Max. gleichzeitig", min(10, selected_batch['count']), "⚡")
        with col3:
            metadata = selected_batch.get('metadata', {})
            generated_date = metadata.get('generated_at', 'Unknown')
            if generated_date != 'Unknown':
                try:
                    date_obj = datetime.fromisoformat(generated_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime("%d.%m.%Y")
                    st.metric("Generiert", formatted_date)
                except:
                    st.metric("Generiert", "Unknown")
            else:
                st.metric("Generiert", "Unknown")
        
        # Initialize chat history for batch
        if "batch_chat_history" not in st.session_state:
            st.session_state.batch_chat_history = []
        
        if "current_batch" not in st.session_state or st.session_state.current_batch != selected_display_name:
            st.session_state.current_batch = selected_display_name
            st.session_state.batch_chat_history = []
        
        # Chat interface
        st.subheader(f"💭 Chat mit {selected_batch['count']} Personas")
        
        # Display chat history
        for chat_item in st.session_state.batch_chat_history:
            st.markdown(f"**Du:** {chat_item['question']}")
            display_batch_responses(chat_item['responses'])
            st.markdown("---")
        
        # Chat input
        user_input = st.text_input("Frage an alle Personas:", key="batch_chat_input", placeholder="z.B. 'Was haltet ihr von einer Banking-App mit KI-Assistent?'")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            send_button = st.button("📤 Senden", key="send_batch")
        
        if send_button and user_input:
            with st.spinner(f"Antworten von {min(10, selected_batch['count'])} Personas werden generiert..."):
                responses = get_batch_responses(selected_batch, user_input, api_key)
                
                # Add to chat history
                st.session_state.batch_chat_history.append({
                    'question': user_input,
                    'responses': responses,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Clear input and rerun to show results
                st.rerun()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("�️ Chat löschen", key="clear_batch_chat"):
                st.session_state.batch_chat_history = []
                st.rerun()
        
        with col2:
            if st.button("� Zusammenfassung", key="summary_batch_chat"):
                if st.session_state.batch_chat_history:
                    show_batch_summary(st.session_state.batch_chat_history, selected_batch)
                else:
                    st.warning("Keine Chat-Daten für Zusammenfassung vorhanden.")

if __name__ == "__main__":
    batch_chat_page()