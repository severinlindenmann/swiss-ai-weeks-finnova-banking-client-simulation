import streamlit as st
import pandas as pd
from pathlib import Path
from data import load_demographie_csv
from llm import SwissAIClient
import random

# Set up the page
st.set_page_config(
    page_title="Banking Persona Generator",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banking Persona Generator")
st.write("Generate realistic banking personas based on demographic data from Switzerland.")

# Initialize session state
if 'persona_generated' not in st.session_state:
    st.session_state.persona_generated = False
if 'current_persona' not in st.session_state:
    st.session_state.current_persona = ""
if 'current_person_data' not in st.session_state:
    st.session_state.current_person_data = {}

def load_prompt_files():
    """Load system and prompt markdown files"""
    system_path = Path(__file__).parent / "system.md"
    prompt_path = Path(__file__).parent / "prompt.md"
    
    with open(system_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    return system_prompt, prompt_template

def format_person_data(person_row):
    """Format person data for display and LLM input"""
    person_dict = person_row.to_dict()
    
    # Create a formatted string for the LLM
    formatted_data = []
    for key, value in person_dict.items():
        if pd.notna(value):  # Only include non-null values
            formatted_data.append(f"{key}: {value}")
    
    return "\n".join(formatted_data), person_dict

def generate_persona():
    """Generate a new persona by selecting a random person and calling the LLM"""
    try:
        # Load data
        df = load_demographie_csv()
        
        # Select a random person
        random_index = random.randint(0, len(df) - 1)
        selected_person = df.iloc[random_index]
        
        # Format person data
        person_data_str, person_dict = format_person_data(selected_person)
        
        # Load prompts
        system_prompt, prompt_template = load_prompt_files()
        
        # Replace placeholder in prompt with actual person data
        full_prompt = prompt_template.replace("{PersonData}", person_data_str)
        
        # Initialize LLM client
        client = SwissAIClient()
        
        # Generate persona
        with st.spinner("Generating persona... This may take a moment."):
            persona = client.complete(
                prompt=full_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2000
            )
        
        # Store in session state
        st.session_state.current_persona = persona
        st.session_state.current_person_data = person_dict
        st.session_state.persona_generated = True
        
        return True
        
    except Exception as e:
        st.error(f"Error generating persona: {str(e)}")
        return False

# Main interface
col1, col2 = st.columns([1, 3])

with col1:
    st.write("### Actions")
    if st.button("🎯 Generate Persona", type="primary", use_container_width=True):
        generate_persona()
    
    if st.session_state.persona_generated:
        st.write("### Source Data")
        st.write("**Selected Person Data:**")
        
        # Display some key demographics in a nice format
        person_data = st.session_state.current_person_data
        
        if person_data:
            # Create a more readable display of key data
            display_data = {}
            key_mappings = {
                'alter': 'Age',
                'bruttojahr': 'Annual Income (CHF)',
                'hhgroesse': 'Household Size',
                'weiblich': 'Gender',
                'ausbildung': 'Education',
                'beruf': 'Profession',
                'kanton': 'Canton',
                'arbeit': 'Employed',
                'kinder': 'Has Children',
                'ledig': 'Single'
            }
            
            for key, label in key_mappings.items():
                if key in person_data and pd.notna(person_data[key]):
                    value = person_data[key]
                    # Format specific fields
                    if key == 'weiblich':
                        value = 'Female' if value == 1 else 'Male'
                    elif key in ['arbeit', 'kinder', 'ledig']:
                        value = 'Yes' if value == 1 else 'No'
                    elif key == 'bruttojahr' and isinstance(value, (int, float)):
                        value = f"{value:,.0f}"
                    
                    display_data[label] = value
            
            for label, value in display_data.items():
                st.write(f"**{label}:** {value}")

with col2:
    if st.session_state.persona_generated:
        st.write("### Generated Banking Persona")
        
        # Display the generated persona in a nice container
        with st.container():
            st.markdown(st.session_state.current_persona)
        
        # Add a button to copy the persona
        if st.button("📋 Copy Persona to Clipboard"):
            st.write("Persona copied! (Note: You may need to manually copy the text above)")
    else:
        st.write("### Welcome!")
        st.write("Click the **Generate Persona** button to create a banking persona based on real Swiss demographic data.")
        st.write("Each persona is generated from a randomly selected person's demographic profile and creates a realistic banking customer profile.")
        
        # Show some info about what the app does
        with st.expander("ℹ️ How it works"):
            st.write("""
            1. **Random Selection**: The app selects a random person from Swiss demographic data
            2. **Data Processing**: Key demographic information is extracted and formatted
            3. **AI Generation**: The demographic data is sent to an AI model along with specialized prompts
            4. **Persona Creation**: A detailed banking persona is generated, including financial behavior, preferences, and characteristics
            """)

# Footer
st.write("---")
st.write("*Banking Persona Generator - Swiss AI Weeks Project*")