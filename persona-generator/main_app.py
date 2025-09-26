import streamlit as st

# Set up the page
st.set_page_config(
    page_title="Banking Persona Generator",
    page_icon="🏦",
    layout="wide"
)

# Page navigation
st.sidebar.title("🏦 Banking Persona Generator")
page = st.sidebar.selectbox(
    "Choose a page",
    ["Single Persona", "Batch Generation", "Persona Library", "Persona Chat", "Batch Chat"]
)

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