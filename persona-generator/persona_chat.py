import streamlit as st
import json
import os
from datetime import datetime
from llm import SwissAIClient
import glob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_all_personas():
    """Load all generated personas from JSON files"""
    personas = []
    
    # Check if generated_personas directory exists
    personas_dir = "generated_personas"
    if not os.path.exists(personas_dir):
        return []
    
    # Load personas from individual files
    for filename in glob.glob(os.path.join(personas_dir, "persona_*.json")):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                persona_data = json.load(f)
                if isinstance(persona_data, dict) and 'persona' in persona_data:
                    personas.append({
                        'filename': os.path.basename(filename),
                        'data': persona_data
                    })
        except Exception as e:
            st.sidebar.warning(f"Could not load {filename}: {e}")
    
    # Load personas from batch files (new format with metadata)
    for filename in glob.glob(os.path.join(personas_dir, "personas_batch_*.json")):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                batch_file = json.load(f)
                
                # Handle new format with metadata and personas array
                if isinstance(batch_file, dict) and 'personas' in batch_file:
                    personas_list = batch_file['personas']
                    for i, persona_data in enumerate(personas_list):
                        if isinstance(persona_data, dict) and 'persona' in persona_data:
                            personas.append({
                                'filename': f"{os.path.basename(filename)}_persona_{i+1}",
                                'data': persona_data
                            })
                # Handle old format (direct array)
                elif isinstance(batch_file, list):
                    for i, persona_data in enumerate(batch_file):
                        if isinstance(persona_data, dict) and 'persona' in persona_data:
                            personas.append({
                                'filename': f"{os.path.basename(filename)}_persona_{i+1}",
                                'data': persona_data
                            })
        except Exception as e:
            st.sidebar.warning(f"Could not load batch {filename}: {e}")
    
    # Also load from old batch files format
    for filename in glob.glob(os.path.join(personas_dir, "batch_*.json")):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
                if isinstance(batch_data, list):
                    for i, persona_data in enumerate(batch_data):
                        if isinstance(persona_data, dict) and 'persona' in persona_data:
                            personas.append({
                                'filename': f"{os.path.basename(filename)}_persona_{i+1}",
                                'data': persona_data
                            })
        except Exception as e:
            st.sidebar.warning(f"Could not load batch {filename}: {e}")
    
    return personas

def create_persona_chat_prompt(persona_data, conversation_history):
    """Create a system prompt for the persona to respond in character"""
    
    persona = persona_data['persona']
    
    # Extract key characteristics from the actual persona structure
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
    personality = banking.get('personality_traits', [])
    
    # Build comprehensive character description
    system_prompt = f"""Du bist {name}, eine {age}-jährige Person aus der Schweiz.

DEINE IDENTITÄT:
- Beruf: {occupation}
- Verfügbares Einkommen: {income} CHF
- Finanzielle Erfahrung: {financial_exp}
- Persönlichkeit: {', '.join(personality) if personality else 'Nicht spezifiziert'}

DEINE VOLLSTÄNDIGEN DATEN:
{json.dumps(persona, indent=2, ensure_ascii=False)}

VERHALTEN:
- Antworte IMMER als diese Person in der ersten Person ("Ich...")
- Verwende die spezifischen Details aus deinen Daten
- Sei konsistent mit deiner Persönlichkeit und deinem Hintergrund
- Antworte auf Deutsch (Schweizerdeutsch ist ok)
- Sei authentisch und natürlich in deinen Antworten
- Beziehe dich auf deine finanzielle Situation und Erfahrungen
- Wenn nach Finanzprodukten gefragt, antworte basierend auf deinem Profil
- WICHTIG: Halte deine Antworten kurz und prägnant (1-3 Sätze)

GESPRÄCHSVERLAUF:
{conversation_history}

Antworte nun als {name} auf die folgende Frage oder Aussage:"""

    return system_prompt

def display_persona_info(persona_data):
    """Display key information about the selected persona"""
    persona = persona_data['persona']
    
    col1, col2 = st.columns(2)
    
    basic_info = persona.get('basic_info', {})
    demographics = persona.get('demographics', {})
    professional = persona.get('professional', {})
    financial = persona.get('financial', {})
    banking = persona.get('banking_persona', {})
    
    with col1:
        st.subheader("👤 Demografische Daten")
        st.write(f"**Name:** {basic_info.get('name', 'N/A')}")
        st.write(f"**Alter:** {basic_info.get('age', 'N/A')}")
        st.write(f"**Geschlecht:** {basic_info.get('gender', 'N/A')}")
        st.write(f"**Kanton:** {demographics.get('canton', 'N/A')}")
        st.write(f"**Wohnsituation:** {demographics.get('housing', 'N/A')}")
        
        st.subheader("💼 Berufliche Daten")
        st.write(f"**Beruf:** {professional.get('job_title', 'N/A')}")
        st.write(f"**Branche:** {professional.get('industry', 'N/A')}")
        st.write(f"**Status:** {professional.get('employment_status', 'N/A')}")
    
    with col2:
        st.subheader("💰 Finanzielle Situation")
        st.write(f"**Bruttoeinkommen:** {financial.get('annual_gross_income_chf', 'N/A')} CHF")
        st.write(f"**Einkommenskategorie:** {financial.get('disposable_income_category', 'N/A')}")
        st.write(f"**Vermögenskategorie:** {financial.get('net_worth_category', 'N/A')}")
        st.write(f"**Finanz-Erfahrung:** {financial.get('financial_experience', 'N/A')}")
        
        st.subheader("🎯 Banking-Profil")
        st.write(f"**Risikotoleranz:** {banking.get('risk_tolerance', 'N/A')}")
        st.write(f"**Investment-Interesse:** {banking.get('investment_interest', 'N/A')}")
        
        goals = banking.get('financial_goals', [])
        if goals:
            st.write("**Ziele:**")
            for goal in goals[:2]:
                st.write(f"• {goal}")

def persona_chat_page():
    """Main persona chat page"""
    st.title("💬 Persona Chat")
    st.markdown("Chat mit deinen Banking-Personas!")
    
    # Get API key from environment or user input
    api_key = os.getenv("SWISS_AI_PLATFORM_API_KEY")
    
    if not api_key:
        api_key = st.text_input("Swiss AI API Key", type="password", key="chat_api_key")
        if not api_key:
            st.warning("API Key benötigt.")
            return
    
    # Load personas
    personas = load_all_personas()
    
    if not personas:
        st.warning("Keine Personas gefunden! Generiere zuerst welche.")
        return
    
    # Persona selection
    st.subheader("🎭 Persona wählen")
    
    persona_options = {}
    for persona in personas:
        persona_data = persona['data']['persona']
        basic_info = persona_data.get('basic_info', {})
        professional = persona_data.get('professional', {})
        
        name = basic_info.get('name', 'Unbekannt')
        age = basic_info.get('age', 'N/A')
        job = professional.get('job_title', 'N/A')
        display_name = f"{name} ({age} Jahre, {job})"
        persona_options[display_name] = persona
    
    selected_display_name = st.selectbox(
        "Persona:",
        list(persona_options.keys()),
        key="persona_selector"
    )
    
    if selected_display_name:
        selected_persona = persona_options[selected_display_name]
        
        # Display persona information
        with st.expander("📋 Details"):
            display_persona_info(selected_persona['data'])
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        if "current_persona" not in st.session_state or st.session_state.current_persona != selected_display_name:
            st.session_state.current_persona = selected_display_name
            st.session_state.chat_history = []
            name = selected_persona['data']['persona'].get('basic_info', {}).get('name', 'die Persona')
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Hallo! Ich bin {name}. Schön, dass du mit mir sprechen möchtest! Was möchtest du wissen?"
            })
        
        # Chat interface
        st.subheader(f"💭 Chat mit {selected_display_name}")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Frage stellen...")
        
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_input
            })
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Prepare conversation history for context
            conversation_context = "\n".join([
                f"{'Benutzer' if msg['role'] == 'user' else 'Persona'}: {msg['content']}" 
                for msg in st.session_state.chat_history[-10:]  # Last 10 messages for context
            ])
            
            # Generate persona response
            with st.chat_message("assistant"):
                with st.spinner("Antwort wird generiert..."):
                    try:
                        system_prompt = create_persona_chat_prompt(
                            selected_persona['data'], 
                            conversation_context
                        )
                        
                        client = SwissAIClient(api_key=api_key)
                        response = client.complete(
                            prompt=user_input,
                            system_prompt=system_prompt,
                            temperature=0.7,
                            max_tokens=200  # Shorter responses
                        )
                        
                        if response:
                            st.write(response)
                            
                            # Add assistant response to history
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": response
                            })
                        else:
                            st.error("Fehler bei der Antwort.")
                    
                    except Exception as e:
                        st.error(f"Fehler: {str(e)}")
        
        # Clear chat button
        if st.button("🗑️ Chat löschen", key="clear_chat"):
            st.session_state.chat_history = []
            name = selected_persona['data']['persona'].get('basic_info', {}).get('name', 'die Persona')
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"Hallo! Ich bin {name}. Schön, dass du mit mir sprechen möchtest! Was möchtest du wissen?"
            })
            st.rerun()
        


if __name__ == "__main__":
    persona_chat_page()