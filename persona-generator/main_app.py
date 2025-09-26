import streamlit as st
from ui_components import load_custom_css, create_header

# Set up the page
st.set_page_config(
    page_title="Banking Persona Generator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Main header
create_header(
    "Banking Persona Generator", 
    "Erstelle realistische Banking-Personas basierend auf Schweizer Daten",
    "🏦"
)

# Enhanced sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%); 
                border-radius: 10px; margin-bottom: 2rem; color: white;">
        <h3 style="margin: 0; color: white;">📋 Navigation</h3>
        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Wähle eine Seite aus</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Page descriptions for better UX
    page_descriptions = {
        "Single Persona": "� Einzelne Persona erstellen",
        "Batch Generation": "📦 Mehrere Personas generieren", 
        "Persona Library": "📚 Persona Bibliothek durchsuchen",
        "Persona Chat": "💬 Mit Personas chatten",
        "Batch Chat": "👥 Batch Chat mit mehreren Personas"
    }
    
    page = st.selectbox(
        "Aktuelle Seite:",
        list(page_descriptions.keys()),
        format_func=lambda x: page_descriptions[x],
        help="Navigiere zwischen den verschiedenen Funktionen"
    )
    
    # Add page info in sidebar
    st.markdown("---")
    st.markdown("### ℹ️ Seiten-Info")
    
    page_info = {
        "Single Persona": "Erstelle eine detaillierte Banking-Persona mit individuellen Eigenschaften.",
        "Batch Generation": "Generiere mehrere Personas gleichzeitig für umfassende Analysen.",
        "Persona Library": "Durchsuche und verwalte alle erstellten Personas.",
        "Persona Chat": "Führe Gespräche mit generierten Personas über Banking-Themen.",
        "Batch Chat": "Stelle Fragen an mehrere Personas gleichzeitig."
    }
    
    st.info(page_info[page])

if page == "Single Persona":
    import single_persona
    single_persona.show()
elif page == "Batch Generation":
    import batch_generation  
    batch_generation.show()
elif page == "Persona Library":
    import persona_library
    persona_library.show()
elif page == "Persona Chat":
    import persona_chat
    persona_chat.persona_chat_page()
elif page == "Batch Chat":
    import batch_chat
    batch_chat.batch_chat_page()