import streamlit as st
import pandas as pd
from pathlib import Path
from data import load_demographie_csv
from llm import SwissAIClient
import random
import json

def load_prompt_files():
    """Load system and prompt markdown files"""
    system_path = Path(__file__).parent / "system.md"
    prompt_path = Path(__file__).parent / "prompt.md"
    
    with open(system_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    return system_prompt, prompt_template

def format_person_data(person_row, additional_params):
    """Format person data for display and LLM input"""
    person_dict = person_row.to_dict()
    
    # Create a formatted string for the statistical data
    formatted_data = []
    for key, value in person_dict.items():
        if pd.notna(value):  # Only include non-null values
            formatted_data.append(f"{key}: {value}")
    
    statistical_data_str = "\n".join(formatted_data)
    
    # Combine with additional parameters
    combined_dict = {**person_dict, **additional_params}
    
    return statistical_data_str, combined_dict

def generate_persona(additional_params, csv_filters, debug_mode=False):
    """Generate a new persona by selecting a random person and calling the LLM"""
    try:
        # Load data
        df = load_demographie_csv()
        
        # Apply CSV filters if any
        filtered_df = df.copy()
        for key, value in csv_filters.items():
            if value is not None and value != "Alle":
                if key in ['alter_min', 'alter_max']:
                    continue  # Handle age range separately
                elif key == 'alter_range':
                    if value != "Alle":
                        if value == "18-25":
                            filtered_df = filtered_df[(filtered_df['alter'] >= 18) & (filtered_df['alter'] <= 25)]
                        elif value == "26-35":
                            filtered_df = filtered_df[(filtered_df['alter'] >= 26) & (filtered_df['alter'] <= 35)]
                        elif value == "36-45":
                            filtered_df = filtered_df[(filtered_df['alter'] >= 36) & (filtered_df['alter'] <= 45)]
                        elif value == "46-65":
                            filtered_df = filtered_df[(filtered_df['alter'] >= 46) & (filtered_df['alter'] <= 65)]
                        elif value == "65+":
                            filtered_df = filtered_df[filtered_df['alter'] > 65]
                elif key == 'geschlecht':
                    if value == "Männlich":
                        filtered_df = filtered_df[filtered_df['weiblich'] == 0]
                    elif value == "Weiblich":
                        filtered_df = filtered_df[filtered_df['weiblich'] == 1]
                elif key == 'bruttojahr_range':
                    if value == "< 60k":
                        filtered_df = filtered_df[filtered_df['bruttojahr'] < 60000]
                    elif value == "60k-100k":
                        filtered_df = filtered_df[(filtered_df['bruttojahr'] >= 60000) & (filtered_df['bruttojahr'] <= 100000)]
                    elif value == "> 100k":
                        filtered_df = filtered_df[filtered_df['bruttojahr'] > 100000]
                else:
                    # Direct column matching
                    if key in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df[key] == value]
        
        if len(filtered_df) == 0:
            st.error("Keine Personen mit den gewählten Filtern gefunden. Bitte lockern Sie die Filter.")
            return None, None
            
        st.info(f"Filter angewendet: {len(filtered_df)} von {len(df)} Personen gefunden")
        
        # Select a random person from filtered data
        random_index = random.randint(0, len(filtered_df) - 1)
        selected_person = filtered_df.iloc[random_index]
        
        # Format person data
        statistical_data_str, combined_dict = format_person_data(selected_person, additional_params)
        
        # Load prompts
        system_prompt, prompt_template = load_prompt_files()
        
        # Extract values from combined data for template replacement
        alter = combined_dict.get('alter', 'N/A')
        geschlecht = 'w' if combined_dict.get('weiblich', 0) == 1 else 'm'
        vermoegen = additional_params.get('vermoegen', 'N/A')
        verfuegbares_einkommen = additional_params.get('verfuegbares_einkommen', 'N/A')
        grosse_ausgaben = additional_params.get('grosse_ausgaben', 'N/A')
        beruf = combined_dict.get('beruf', 'N/A')
        kinder = combined_dict.get('kinder', 0)
        eigentum = additional_params.get('eigentum', 'N/A')
        single = combined_dict.get('ledig', 0)
        finanz_erfahrung = additional_params.get('finanz_erfahrung', 'N/A')
        
        # Replace all placeholders in prompt template
        full_prompt = prompt_template.format(
            statistical_data=statistical_data_str,
            alter=alter,
            geschlecht=geschlecht,
            vermoegen=vermoegen,
            verfuegbares_einkommen=verfuegbares_einkommen,
            grosse_ausgaben=grosse_ausgaben,
            beruf=beruf,
            kinder=kinder,
            eigentum=eigentum,
            single=single,
            finanz_erfahrung=finanz_erfahrung
        )
        
        # Show debug info if enabled
        if debug_mode:
            with st.expander("🔍 Debug: Full Prompt Sent to LLM"):
                st.text("System Prompt:")
                st.code(system_prompt, language="text")
                st.text("User Prompt:")
                st.code(full_prompt, language="text")
        
        # Initialize LLM client
        client = SwissAIClient()
        
        # Generate persona
        with st.spinner("Generating persona... This may take a moment."):
            persona_response = client.complete(
                prompt=full_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=3000
            )
            
            # Clean up response - remove potential markdown formatting and whitespace
            persona_clean = persona_response.strip()
            
            # Remove markdown code blocks
            if persona_clean.startswith("```json"):
                persona_clean = persona_clean[7:]
            elif persona_clean.startswith("```"):
                persona_clean = persona_clean[3:]
            if persona_clean.endswith("```"):
                persona_clean = persona_clean[:-3]
            
            # Clean whitespace and newlines
            persona_clean = persona_clean.strip()
            
            # Try to find JSON object start if response has extra text
            json_start = persona_clean.find('{')
            json_end = persona_clean.rfind('}')
            
            if json_start != -1 and json_end != -1 and json_end > json_start:
                persona_clean = persona_clean[json_start:json_end+1]
            
            # Validate JSON
            try:
                parsed_json = json.loads(persona_clean)
                st.success("✅ Valid JSON generated!")
                return persona_clean, combined_dict
            except json.JSONDecodeError as e:
                st.error(f"❌ LLM returned invalid JSON: {str(e)}")
                
                # Show debugging information (always show if debug mode, or in expander otherwise)
                if debug_mode:
                    st.text("Raw LLM response:")
                    st.code(persona_response, language="text")
                    st.text("Cleaned response:")
                    st.code(persona_clean, language="text")
                    st.text(f"JSON error at position {e.pos}: {e.msg}")
                else:
                    with st.expander("🔍 Debug Information"):
                        st.text("Raw LLM response:")
                        st.code(persona_response, language="text")
                        st.text("Cleaned response:")
                        st.code(persona_clean, language="text")
                        st.text(f"JSON error at position {e.pos}: {e.msg}")
                
                # Try to fix common JSON issues
                try:
                    import re
                    
                    # Remove JavaScript-style comments (// comment)
                    fixed_json = re.sub(r'//.*$', '', persona_clean, flags=re.MULTILINE)
                    
                    # Remove trailing commas
                    fixed_json = re.sub(r',\s*}', '}', fixed_json)
                    fixed_json = re.sub(r',\s*]', ']', fixed_json)
                    
                    # Remove extra whitespace
                    fixed_json = re.sub(r'\n\s*\n', '\n', fixed_json)
                    
                    parsed_json = json.loads(fixed_json)
                    persona_clean = fixed_json
                    st.warning("⚠️ Auto-fixed JSON formatting issues (removed comments)")
                    return persona_clean, combined_dict
                except Exception as fix_error:
                    if debug_mode:
                        st.error(f"Failed to auto-fix JSON: {fix_error}")
                    return None, None
        
    except Exception as e:
        st.error(f"Error generating persona: {str(e)}")
        return None, None

# Load data once for filter options
@st.cache_data
def get_filter_options():
    df = load_demographie_csv()
    return {
        'kantone': sorted([k for k in df['kanton'].unique() if pd.notna(k)]),
        'ausbildung': sorted([a for a in df['ausbildung'].unique() if pd.notna(a)]),
        'beruf': sorted([b for b in df['beruf'].unique() if pd.notna(b)]),
        'sprachgebiet': sorted([s for s in df['sprachgebiet'].unique() if pd.notna(s)])
    }

def show():
    """Show the single persona generation page"""
    
    # Initialize session state
    if 'persona_generated' not in st.session_state:
        st.session_state.persona_generated = False
    if 'current_persona' not in st.session_state:
        st.session_state.current_persona = ""
    if 'current_person_data' not in st.session_state:
        st.session_state.current_person_data = {}

    st.title("👤 Single Persona Generator")
    st.write("Generate one realistic banking persona based on Swiss demographic data with customizable filters.")

    filter_options = get_filter_options()

    # Main interface
    col1, col2 = st.columns([1, 3])

    with col1:
        # Debug mode toggle
        debug_mode = st.checkbox("🐛 Debug Mode", help="Shows detailed LLM responses for troubleshooting")
        
        st.write("### CSV-Daten Filter")
        
        # Demographics filters from CSV
        st.write("**Demografische Filter:**")
        
        alter_range = st.selectbox(
            "Altersgruppe",
            options=["Alle", "18-25", "26-35", "36-45", "46-65", "65+"],
            index=0,
            help="Wählen Sie eine Altersgruppe"
        )
        
        geschlecht_filter = st.selectbox(
            "Geschlecht",
            options=["Alle", "Männlich", "Weiblich"],
            index=0,
            help="Filtern nach Geschlecht"
        )
        
        kanton_filter = st.selectbox(
            "Kanton",
            options=["Alle"] + filter_options['kantone'],
            index=0,
            help="Filtern nach Kanton"
        )
        
        sprachgebiet_filter = st.selectbox(
            "Sprachgebiet", 
            options=["Alle"] + filter_options['sprachgebiet'],
            index=0,
            help="Filtern nach Sprachgebiet"
        )
        
        bruttojahr_range = st.selectbox(
            "Bruttojahreseinkommen",
            options=["Alle", "< 60k", "60k-100k", "> 100k"],
            index=0,
            help="Filtern nach Einkommensbereich"
        )
        
        ausbildung_filter = st.selectbox(
            "Ausbildung",
            options=["Alle"] + filter_options['ausbildung'][:10],  # Limit to first 10 for UI
            index=0,
            help="Filtern nach Ausbildung"
        )
        
        erwerbstaetig_filter = st.selectbox(
            "Erwerbstätigkeit",
            options=["Alle", "Erwerbstätig", "Nicht erwerbstätig"],
            index=0,
            help="Filtern nach Erwerbsstatus"
        )
        
        kinder_filter = st.selectbox(
            "Kinder im Haushalt",
            options=["Alle", "Mit Kindern", "Ohne Kinder"],
            index=0,
            help="Filtern nach Kindern im Haushalt"
        )
        
        # Collect CSV filters
        csv_filters = {
            'alter_range': alter_range,
            'geschlecht': geschlecht_filter,
            'kanton': kanton_filter if kanton_filter != "Alle" else None,
            'sprachgebiet': sprachgebiet_filter if sprachgebiet_filter != "Alle" else None,
            'bruttojahr_range': bruttojahr_range,
            'ausbildung': ausbildung_filter if ausbildung_filter != "Alle" else None,
            'arbeit': 1 if erwerbstaetig_filter == "Erwerbstätig" else (0 if erwerbstaetig_filter == "Nicht erwerbstätig" else None),
            'kinder': 1 if kinder_filter == "Mit Kindern" else (0 if kinder_filter == "Ohne Kinder" else None)
        }
        
        st.write("---")
        
        st.write("### Banking Parameter")
        
        # Additional parameters not in CSV data
        st.write("**Banking-spezifische Parameter:**")
        
        vermoegen = st.selectbox(
            "Freies Vermögen",
            options=["< 10k", "10k-100k", ">100k"],
            index=0,
            help="Geschätztes freies Vermögen der Person"
        )
        
        verfuegbares_einkommen = st.selectbox(
            "Verfügbares Einkommen (Einkommen - Ausgaben)",
            options=["< 60k", "60k-100k", ">100k"],
            index=0,
            help="Verfügbares Einkommen nach Abzug der Lebenshaltungskosten"
        )
        
        grosse_ausgaben = st.selectbox(
            "Geplante größere Ausgaben/Investitionen",
            options=["ja", "nein"],
            index=1,
            help="Plant die Person größere Ausgaben oder Investitionen?"
        )
        
        eigentum = st.selectbox(
            "Wohnsituation",
            options=["Eigentum", "Miete"],
            index=1,
            help="Besitzt die Person Wohneigentum oder mietet sie?"
        )
        
        finanz_erfahrung = st.selectbox(
            "Erfahrung mit Finanzprodukten",
            options=["Einsteiger", "Fortgeschritten", "Experte"],
            index=1,
            help="Wie erfahren ist die Person im Umgang mit Finanzprodukten?"
        )
        
        # Collect all additional parameters
        additional_params = {
            'vermoegen': vermoegen,
            'verfuegbares_einkommen': verfuegbares_einkommen,
            'grosse_ausgaben': grosse_ausgaben,
            'eigentum': 1 if eigentum == "Eigentum" else 0,
            'finanz_erfahrung': finanz_erfahrung
        }
        
        st.write("---")
        
        st.write("### Actions")
        if st.button("🎯 Generate Persona", type="primary", use_container_width=True):
            persona, person_data = generate_persona(additional_params, csv_filters, debug_mode)
            if persona and person_data:
                st.session_state.current_persona = persona
                st.session_state.current_person_data = person_data
                st.session_state.persona_generated = True

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
                    'ledig': 'Single',
                    'vermoegen': 'Net Worth',
                    'verfuegbares_einkommen': 'Disposable Income',
                    'grosse_ausgaben': 'Major Expenses Planned',
                    'eigentum': 'Housing',
                    'finanz_erfahrung': 'Financial Experience'
                }
                
                for key, label in key_mappings.items():
                    if key in person_data and pd.notna(person_data[key]):
                        value = person_data[key]
                        # Format specific fields
                        if key == 'weiblich':
                            value = 'Female' if value == 1 else 'Male'
                        elif key in ['arbeit', 'kinder', 'ledig']:
                            value = 'Yes' if value == 1 else 'No'
                        elif key == 'eigentum':
                            value = 'Owner' if value == 1 else 'Renter'
                        elif key == 'bruttojahr' and isinstance(value, (int, float)):
                            value = f"{value:,.0f}"
                        
                        display_data[label] = value
                
                for label, value in display_data.items():
                    st.write(f"**{label}:** {value}")

    with col2:
        if st.session_state.persona_generated:
            st.write("### Generated Banking Persona")
            
            # Try to parse JSON and display structured, fallback to raw text
            try:
                persona_json = json.loads(st.session_state.current_persona)
                
                # Display structured persona data
                if isinstance(persona_json, dict):
                    # Basic Info
                    if "basic_info" in persona_json:
                        st.subheader("👤 Basic Information")
                        basic = persona_json["basic_info"]
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Name:** {basic.get('name', 'N/A')}")
                            st.write(f"**Age:** {basic.get('age', 'N/A')}")
                            st.write(f"**Gender:** {basic.get('gender', 'N/A')}")
                        with col_b:
                            st.write(f"**Nationality:** {basic.get('nationality', 'N/A')}")
                            st.write(f"**Languages:** {', '.join(basic.get('languages', []))}")
                    
                    # Banking Persona
                    if "banking_persona" in persona_json:
                        st.subheader("🏦 Banking Profile")
                        banking = persona_json["banking_persona"]
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Risk Tolerance:** {banking.get('risk_tolerance', 'N/A')}")
                            st.write(f"**Investment Interest:** {banking.get('investment_interest', 'N/A')}")
                            st.write(f"**Banking Frequency:** {banking.get('banking_frequency', 'N/A')}")
                        with col_b:
                            prefs = banking.get('banking_preferences', {})
                            st.write(f"**Channel Preference:** {prefs.get('channel_preference', 'N/A')}")
                            st.write(f"**Service Level:** {prefs.get('service_level', 'N/A')}")
                            st.write(f"**Product Complexity:** {prefs.get('product_complexity', 'N/A')}")
                    
                    # Financial Goals
                    if "banking_persona" in persona_json and "financial_goals" in persona_json["banking_persona"]:
                        st.subheader("🎯 Financial Goals")
                        goals = persona_json["banking_persona"]["financial_goals"]
                        for goal in goals:
                            st.write(f"• {goal}")
                    
                    # Narrative
                    if "narrative" in persona_json:
                        st.subheader("📖 Life Story")
                        narrative = persona_json["narrative"]
                        st.write(f"**Background:** {narrative.get('life_story', 'N/A')}")
                        st.write(f"**Current Situation:** {narrative.get('current_situation', 'N/A')}")
                        st.write(f"**Future Aspirations:** {narrative.get('future_aspirations', 'N/A')}")
                    
                    # Raw JSON in expander
                    with st.expander("📄 View Full JSON"):
                        st.json(persona_json)
                else:
                    st.markdown(st.session_state.current_persona)
                    
            except (json.JSONDecodeError, TypeError):
                # Fallback to raw text display
                st.markdown(st.session_state.current_persona)
            
            # Add download button for JSON
            if st.button("💾 Download Persona JSON"):
                try:
                    persona_json = json.loads(st.session_state.current_persona)
                    st.download_button(
                        label="Download JSON File",
                        data=json.dumps(persona_json, indent=2, ensure_ascii=False),
                        file_name=f"persona_{persona_json.get('persona_id', 'unknown')}.json",
                        mime="application/json"
                    )
                except:
                    st.error("Could not parse persona as JSON for download.")
        else:
            st.write("### Welcome!")
            st.write("Configure filters and banking parameters on the left, then click **Generate Persona** to create realistic banking customers.")
            st.write("Each persona combines real Swiss demographic data with AI-generated banking behavior patterns.")
            
            # Show some info about what the app does
            with st.expander("ℹ️ How it works"):
                st.write("""
                1. **Filter Selection**: Choose demographic criteria from real Swiss census data
                2. **Banking Parameters**: Add banking-specific attributes not in demographic data  
                3. **AI Generation**: Combined data is sent to Swiss AI platform with specialized prompts
                4. **Persona Creation**: Generates detailed banking persona with behaviors, preferences, and life story
                5. **Structured Output**: Results displayed as organized JSON with key banking insights
                """)
                
            with st.expander("🔧 Available Filters"):
                st.write("""
                **CSV Data Filters:**
                - Age groups, Gender, Canton, Language region
                - Income brackets, Education level, Employment status
                - Children in household
                
                **Banking Parameters:**
                - Net worth category, Disposable income
                - Major expense plans, Housing situation
                - Financial product experience level
                """)