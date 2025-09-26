import streamlit as st
import json
import pandas as pd
from typing import Dict, List, Any

# Page configuration
st.set_page_config(
    page_title="Banking Client Personas",
    page_icon="🏦",
    layout="wide"
)

# Function to load persona data
@st.cache_data
def load_personas() -> List[Dict[str, Any]]:
    """Load personas from the JSON file"""
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['personas']
    except FileNotFoundError:
        st.error("data.json file not found!")
        return []
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

# Function to assign emojis based on profession
def get_persona_emoji(profession: str, age: int, family_status: str) -> str:
    """Assign emoji based on profession and characteristics"""
    profession_lower = profession.lower()
    
    # Profession-based emojis
    if "teacher" in profession_lower or "education" in profession_lower:
        return "👩‍🏫"
    elif "doctor" in profession_lower or "nurse" in profession_lower:
        return "👩‍⚕️"
    elif "engineer" in profession_lower:
        return "👩‍💻"
    elif "lawyer" in profession_lower:
        return "👩‍💼"
    elif "pilot" in profession_lower:
        return "👩‍✈️"
    elif "artist" in profession_lower or "designer" in profession_lower:
        return "👩‍🎨"
    elif "researcher" in profession_lower or "scientist" in profession_lower:
        return "👩‍🔬"
    elif "manager" in profession_lower or "consultant" in profession_lower:
        return "👔"
    elif "entrepreneur" in profession_lower:
        return "💼"
    elif "musician" in profession_lower:
        return "🎵"
    elif "professor" in profession_lower:
        return "👨‍🎓"
    elif "architect" in profession_lower:
        return "📐"
    elif "contractor" in profession_lower or "manufacturer" in profession_lower:
        return "👷‍♂️"
    elif "pharmacist" in profession_lower:
        return "💊"
    elif "civil servant" in profession_lower:
        return "🏛️"
    elif "retired" in profession_lower:
        return "🧓"
    else:
        # Default based on age and family status
        if age >= 60:
            return "🧓"
        elif age >= 40:
            return "👨‍💼" if "married" in family_status else "👩‍💼"
        elif age >= 30:
            return "👨" if "married" in family_status else "👩"
        else:
            return "🧑"

# Function to format currency
def format_currency(amount: int) -> str:
    """Format currency amounts in CHF"""
    return f"CHF {amount:,}"

# Function to get risk color
def get_risk_color(risk_tolerance: str) -> str:
    """Get color code for risk tolerance"""
    colors = {
        "low": "🟢",
        "medium": "🟡", 
        "high": "🔴"
    }
    return colors.get(risk_tolerance.lower(), "⚪")

# Function to display persona card
def display_persona_card(persona: Dict[str, Any], key_suffix: str = ""):
    """Display a persona in a card format"""
    emoji = get_persona_emoji(persona['profession'], persona['age'], persona['family_status'])
    
    with st.container():
        st.markdown(f"### {emoji} {persona['name']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Age:** {persona['age']}")
            st.markdown(f"**Profession:** {persona['profession']}")
            st.markdown(f"**Location:** {persona['location']}")
            st.markdown(f"**Family Status:** {persona['family_status']}")
            st.markdown(f"**Risk Tolerance:** {get_risk_color(persona['risk_tolerance'])} {persona['risk_tolerance'].title()}")
        
        with col2:
            st.markdown(f"**Annual Income:** {format_currency(persona['annual_income'])}")
            st.markdown(f"**Current Assets:** {format_currency(persona['current_assets'])}")
            st.markdown(f"**Monthly Expenses:** {format_currency(persona['monthly_expenses'])}")
            
            # Calculate net worth and savings rate
            net_worth = persona['current_assets']
            annual_savings = persona['annual_income'] - (persona['monthly_expenses'] * 12)
            savings_rate = (annual_savings / persona['annual_income']) * 100 if persona['annual_income'] > 0 else 0
            
            st.markdown(f"**Net Worth:** {format_currency(net_worth)}")
            st.markdown(f"**Savings Rate:** {savings_rate:.1f}%")
        
        # Financial Goals
        st.markdown("**Financial Goals:**")
        for goal in persona['financial_goals']:
            st.markdown(f"• {goal}")
        
        # Banking Preferences
        st.markdown("**Banking Preferences:**")
        for pref in persona['banking_preferences']:
            st.markdown(f"• {pref}")

# Main application
def main():
    # Title
    st.title("🏦 Banking Client Personas Visualization")
    st.markdown("---")
    
    # Load data
    personas = load_personas()
    
    if not personas:
        st.stop()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Mode selection
    mode = st.sidebar.radio("Choose Mode:", ["Single Persona View", "Compare Personas", "All Personas Overview"])
    
    if mode == "Single Persona View":
        st.header("👤 Single Persona View")
        
        # Persona selection
        persona_names = [f"{p['name']} ({p['profession']})" for p in personas]
        selected_name = st.selectbox("Select a persona:", persona_names)
        
        if selected_name:
            selected_index = persona_names.index(selected_name)
            selected_persona = personas[selected_index]
            
            display_persona_card(selected_persona)
    
    elif mode == "Compare Personas":
        st.header("🔍 Compare Personas")
        
        persona_names = [f"{p['name']} ({p['profession']})" for p in personas]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Persona 1")
            selected_name_1 = st.selectbox("Select first persona:", persona_names, key="persona1")
            
        with col2:
            st.subheader("Persona 2")
            selected_name_2 = st.selectbox("Select second persona:", persona_names, key="persona2")
        
        if selected_name_1 and selected_name_2:
            selected_index_1 = persona_names.index(selected_name_1)
            selected_index_2 = persona_names.index(selected_name_2)
            
            persona_1 = personas[selected_index_1]
            persona_2 = personas[selected_index_2]
            
            col1, col2 = st.columns(2)
            
            with col1:
                display_persona_card(persona_1, "_1")
            
            with col2:
                display_persona_card(persona_2, "_2")
            
            # Comparison metrics
            st.markdown("---")
            st.subheader("📊 Quick Comparison")
            
            comparison_data = {
                "Metric": [
                    "Age",
                    "Annual Income",
                    "Current Assets", 
                    "Monthly Expenses",
                    "Risk Tolerance",
                    "Savings Rate"
                ],
                persona_1['name']: [
                    persona_1['age'],
                    format_currency(persona_1['annual_income']),
                    format_currency(persona_1['current_assets']),
                    format_currency(persona_1['monthly_expenses']),
                    persona_1['risk_tolerance'].title(),
                    f"{((persona_1['annual_income'] - persona_1['monthly_expenses'] * 12) / persona_1['annual_income'] * 100):.1f}%"
                ],
                persona_2['name']: [
                    persona_2['age'],
                    format_currency(persona_2['annual_income']),
                    format_currency(persona_2['current_assets']),
                    format_currency(persona_2['monthly_expenses']),
                    persona_2['risk_tolerance'].title(),
                    f"{((persona_2['annual_income'] - persona_2['monthly_expenses'] * 12) / persona_2['annual_income'] * 100):.1f}%"
                ]
            }
            
            comparison_df = pd.DataFrame(comparison_data)
            st.table(comparison_df)
    
    else:  # All Personas Overview
        st.header("📋 All Personas Overview")
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Personas", len(personas))
        
        with col2:
            avg_age = sum(p['age'] for p in personas) / len(personas)
            st.metric("Average Age", f"{avg_age:.1f} years")
        
        with col3:
            avg_income = sum(p['annual_income'] for p in personas) / len(personas)
            st.metric("Average Income", format_currency(int(avg_income)))
        
        with col4:
            avg_assets = sum(p['current_assets'] for p in personas) / len(personas)
            st.metric("Average Assets", format_currency(int(avg_assets)))
        
        # Risk tolerance distribution
        st.subheader("🎯 Risk Tolerance Distribution")
        risk_counts = {}
        for persona in personas:
            risk = persona['risk_tolerance']
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        risk_col1, risk_col2, risk_col3 = st.columns(3)
        with risk_col1:
            st.metric("🟢 Low Risk", risk_counts.get('low', 0))
        with risk_col2:
            st.metric("🟡 Medium Risk", risk_counts.get('medium', 0))
        with risk_col3:
            st.metric("🔴 High Risk", risk_counts.get('high', 0))
        
        # All personas grid
        st.subheader("👥 All Personas")
        
        # Create a grid layout
        for i in range(0, len(personas), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(personas):
                    with st.expander(f"{get_persona_emoji(personas[i]['profession'], personas[i]['age'], personas[i]['family_status'])} {personas[i]['name']}"):
                        display_persona_card(personas[i], f"_grid_{i}")
            
            with col2:
                if i + 1 < len(personas):
                    with st.expander(f"{get_persona_emoji(personas[i+1]['profession'], personas[i+1]['age'], personas[i+1]['family_status'])} {personas[i+1]['name']}"):
                        display_persona_card(personas[i+1], f"_grid_{i+1}")

if __name__ == "__main__":
    main()