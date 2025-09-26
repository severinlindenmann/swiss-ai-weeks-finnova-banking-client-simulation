import streamlit as st
import json
import os
from datetime import datetime
from llm import SwissAIClient
import glob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Persona Chat - Banking Simulation",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --info-color: #17a2b8;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --light-bg: #f8f9fa;
        --dark-text: #212529;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Persona card styling */
    .persona-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .persona-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 8px 25px rgba(31, 119, 180, 0.15);
        transform: translateY(-2px);
    }
    
    .persona-card.selected {
        border-color: #1f77b4;
        background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
    }
    
    .persona-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    .persona-details {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .persona-tag {
        background: #e9ecef;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #495057;
    }
    
    /* Chat styling */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 10px;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        margin-right: 2rem;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 25px rgba(31, 119, 180, 0.3);
        transform: translateY(-2px);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Hide Streamlit branding */
    .css-15zrgzn {display: none;}
    .css-eczf16 {display: none;}
    .css-jn99sy {display: none;}
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem !important;
        }
        
        .persona-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
        
        .persona-details {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .persona-tag {
            display: inline-block;
            margin: 0.2rem 0;
        }
        
        .metric-container {
            margin: 0.3rem 0;
            padding: 0.8rem;
        }
    }
    
    /* Improved scrolling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Animation for cards */
    .persona-card {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Loading spinner styling */
    .stSpinner > div {
        border-top-color: #1f77b4 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

def display_persona_card(persona_data, is_selected=False):
    """Display a persona as an attractive card"""
    persona = persona_data['persona']
    basic_info = persona.get('basic_info', {})
    professional = persona.get('professional', {})
    financial = persona.get('financial', {})
    
    name = basic_info.get('name', 'Unbekannt')
    age = basic_info.get('age', 'N/A')
    job = professional.get('job_title', 'N/A')
    income = financial.get('disposable_income_category', 'N/A')
    
    card_class = "persona-card selected" if is_selected else "persona-card"
    
    st.markdown(f"""
    <div class="{card_class}">
        <div class="persona-name">👤 {name}</div>
        <div class="persona-details">
            <span class="persona-tag">🎂 {age} Jahre</span>
            <span class="persona-tag">💼 {job}</span>
            <span class="persona-tag">💰 {income} CHF</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_persona_info(persona_data):
    """Display detailed information about the selected persona"""
    persona = persona_data['persona']
    
    basic_info = persona.get('basic_info', {})
    demographics = persona.get('demographics', {})
    professional = persona.get('professional', {})
    financial = persona.get('financial', {})
    banking = persona.get('banking_persona', {})
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["👤 Persönliche Daten", "💼 Beruf & Finanzen", "🎯 Banking-Profil"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <h4>📋 Grunddaten</h4>
                <p><strong>Name:</strong> {basic_info.get('name', 'N/A')}</p>
                <p><strong>Alter:</strong> {basic_info.get('age', 'N/A')} Jahre</p>
                <p><strong>Geschlecht:</strong> {basic_info.get('gender', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <h4>🏠 Wohnsituation</h4>
                <p><strong>Kanton:</strong> {demographics.get('canton', 'N/A')}</p>
                <p><strong>Wohnsituation:</strong> {demographics.get('housing', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <h4>💼 Berufliches</h4>
                <p><strong>Beruf:</strong> {professional.get('job_title', 'N/A')}</p>
                <p><strong>Branche:</strong> {professional.get('industry', 'N/A')}</p>
                <p><strong>Status:</strong> {professional.get('employment_status', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <h4>💰 Finanzielle Lage</h4>
                <p><strong>Bruttoeinkommen:</strong> {financial.get('annual_gross_income_chf', 'N/A')} CHF</p>
                <p><strong>Verfügbares Einkommen:</strong> {financial.get('disposable_income_category', 'N/A')}</p>
                <p><strong>Vermögen:</strong> {financial.get('net_worth_category', 'N/A')}</p>
                <p><strong>Finanz-Erfahrung:</strong> {financial.get('financial_experience', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <h4>📊 Risiko & Investment</h4>
                <p><strong>Risikotoleranz:</strong> {banking.get('risk_tolerance', 'N/A')}</p>
                <p><strong>Investment-Interesse:</strong> {banking.get('investment_interest', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            goals = banking.get('financial_goals', [])
            if goals:
                goals_text = "<br>".join([f"• {goal}" for goal in goals[:3]])
                st.markdown(f"""
                <div class="metric-container">
                    <h4>🎯 Finanzielle Ziele</h4>
                    {goals_text}
                </div>
                """, unsafe_allow_html=True)
            
            personality = banking.get('personality_traits', [])
            if personality:
                personality_text = ", ".join(personality[:3])
                st.markdown(f"""
                <div class="metric-container">
                    <h4>🧠 Persönlichkeit</h4>
                    <p>{personality_text}</p>
                </div>
                """, unsafe_allow_html=True)

def persona_chat_page():
    """Main persona chat page"""
    # Load custom CSS
    load_custom_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💬 Persona Chat</h1>
        <p>Interagiere mit realistischen Banking-Personas basierend auf Schweizer Daten</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get API key from environment or user input
    api_key = os.getenv("SWISS_AI_PLATFORM_API_KEY")
    
    if not api_key:
        st.markdown("""
        <div class="warning-box">
            <strong>🔑 API Key erforderlich</strong><br>
            Bitte gib deinen Swiss AI Platform API Key ein, um zu starten.
        </div>
        """, unsafe_allow_html=True)
        api_key = st.text_input("Swiss AI API Key", type="password", key="chat_api_key", placeholder="Dein API Key hier eingeben...")
        if not api_key:
            return
    
    # Load personas
    personas = load_all_personas()
    
    if not personas:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Keine Personas gefunden!</strong><br>
            Bitte generiere zuerst einige Personas, bevor du mit ihnen chatten kannst.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Persona selection section
    st.markdown("### 🎭 Wähle eine Persona")
    st.markdown("Klicke auf eine der verfügbaren Personas, um ein Gespräch zu beginnen:")
    
    # Create persona selection in sidebar for better UX
    with st.sidebar:
        st.markdown("### 👥 Verfügbare Personas")
        
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
            "Aktuelle Persona:",
            list(persona_options.keys()),
            key="persona_selector",
            help="Wähle eine Persona aus der Liste"
        )
        
        if selected_display_name:
            selected_persona = persona_options[selected_display_name]
            st.markdown("---")
            st.markdown("**📊 Quick Info:**")
            
            persona_data = selected_persona['data']['persona']
            basic_info = persona_data.get('basic_info', {})
            financial = persona_data.get('financial', {})
            banking = persona_data.get('banking_persona', {})
            
            st.markdown(f"**Alter:** {basic_info.get('age', 'N/A')} Jahre")
            st.markdown(f"**Einkommen:** {financial.get('disposable_income_category', 'N/A')}")
            st.markdown(f"**Risiko:** {banking.get('risk_tolerance', 'N/A')}")
    
    if selected_display_name:
        selected_persona = persona_options[selected_display_name]
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Chat interface
            persona_name = selected_persona['data']['persona'].get('basic_info', {}).get('name', 'Persona')
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%); 
                        padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: white;">💭 Chat mit {persona_name}</h3>
                <p style="margin: 0; opacity: 0.9;">Stelle Fragen über Banking, Finanzen oder persönliche Präferenzen</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            if "current_persona" not in st.session_state or st.session_state.current_persona != selected_display_name:
                st.session_state.current_persona = selected_display_name
                st.session_state.chat_history = []
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Hallo! Ich bin {persona_name}. Schön, dass du mit mir sprechen möchtest! Was möchtest du über meine Banking-Bedürfnisse oder Finanzen wissen? 💰"
                })
            
            # Display chat history with custom styling
            chat_container = st.container()
            with chat_container:
                for i, message in enumerate(st.session_state.chat_history):
                    if message["role"] == "user":
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                                    padding: 1rem; margin: 1rem 0 1rem 2rem; border-radius: 10px 10px 5px 10px;">
                            <strong>Du:</strong><br>{message["content"]}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                                    padding: 1rem; margin: 1rem 2rem 1rem 0; border-radius: 10px 10px 10px 5px;">
                            <strong>{persona_name}:</strong><br>{message["content"]}
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            # Display persona card and details
            display_persona_card(selected_persona['data'], True)
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            if st.button("🏦 Banking-Präferenzen", key="banking_prefs", use_container_width=True):
                question = "Was sind deine Banking-Präferenzen und warum nutzt du diese Bank?"
                st.session_state.suggested_question = question
            
            if st.button("💰 Investment-Strategie", key="investment", use_container_width=True):
                question = "Wie ist deine Einstellung zu Investitionen und Geldanlagen?"
                st.session_state.suggested_question = question
                
            if st.button("🎯 Finanzielle Ziele", key="goals", use_container_width=True):
                question = "Was sind deine wichtigsten finanziellen Ziele für die nächsten Jahre?"
                st.session_state.suggested_question = question
            
            # Display detailed persona information
            with st.expander("📋 Detaillierte Informationen", expanded=False):
                display_persona_info(selected_persona['data'])
        
        # Chat input section
        st.markdown("---")
        
        # Handle suggested questions
        if hasattr(st.session_state, 'suggested_question'):
            user_input = st.session_state.suggested_question
            del st.session_state.suggested_question
        else:
            user_input = st.chat_input("💬 Stelle eine Frage... (z.B. 'Wie sparst du dein Geld?' oder 'Welche Bank nutzt du?')")
        
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user", 
                "content": user_input
            })
            
            # Prepare conversation history for context
            conversation_context = "\n".join([
                f"{'Benutzer' if msg['role'] == 'user' else 'Persona'}: {msg['content']}" 
                for msg in st.session_state.chat_history[-10:]  # Last 10 messages for context
            ])
            
            # Generate persona response
            with st.spinner("🤔 Antwort wird generiert..."):
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
                        # Add assistant response to history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response
                        })
                        st.rerun()  # Refresh to show new message
                    else:
                        st.error("❌ Fehler bei der Antwort-Generierung.")
                
                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")
        
        # Chat controls
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Chat löschen", key="clear_chat", use_container_width=True):
                st.session_state.chat_history = []
                persona_name = selected_persona['data']['persona'].get('basic_info', {}).get('name', 'die Persona')
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Hallo! Ich bin {persona_name}. Schön, dass du mit mir sprechen möchtest! Was möchtest du über meine Banking-Bedürfnisse oder Finanzen wissen? 💰"
                })
                st.rerun()
        
        with col2:
            if st.button("📥 Chat exportieren", key="export_chat", use_container_width=True):
                # Create chat export
                chat_export = {
                    "persona": selected_display_name,
                    "timestamp": datetime.now().isoformat(),
                    "messages": st.session_state.chat_history
                }
                st.download_button(
                    label="💾 Download",
                    data=json.dumps(chat_export, indent=2, ensure_ascii=False),
                    file_name=f"chat_{persona_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_chat"
                )
        
    else:
        st.markdown("""
        <div class="info-box">
            <strong>👋 Willkommen beim Persona Chat!</strong><br>
            Wähle eine Persona aus der Seitenleiste, um das Gespräch zu beginnen.
        </div>
        """, unsafe_allow_html=True)
    # Statistics sidebar
    with st.sidebar:
        if selected_display_name and len(st.session_state.chat_history) > 1:
            st.markdown("---")
            st.markdown("### 📊 Chat Statistiken")
            
            user_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "user"]
            assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
            
            st.metric("Deine Nachrichten", len(user_messages))
            st.metric("Persona Antworten", len(assistant_messages) - 1)  # -1 for initial greeting
            
            # Show total conversation length
            total_chars = sum(len(msg["content"]) for msg in st.session_state.chat_history)
            st.metric("Gespräch Länge", f"{total_chars} Zeichen")

if __name__ == "__main__":
    persona_chat_page()