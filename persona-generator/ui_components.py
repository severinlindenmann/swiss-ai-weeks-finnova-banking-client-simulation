"""
Shared UI components and styling for the Banking Persona Generator Streamlit app.
This module provides consistent design elements across all pages.
"""

import streamlit as st

def load_custom_css():
    """Load the modern CSS styling for all Streamlit pages"""
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
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1.5rem 0 1rem 0;
    }
    
    .section-header h3 {
        margin: 0;
        color: #1f77b4;
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
    
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
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
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 0.5rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 10px rgba(31, 119, 180, 0.1);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 10px rgba(31, 119, 180, 0.1);
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%);
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
    
    /* File uploader styling */
    .stFileUploader > div > div {
        border-radius: 10px;
        border: 2px dashed #e9ecef;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #1f77b4;
        background: #f8f9ff;
    }
    
    /* Tabs styling */
    .stTabs > div > div > div > div {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    
    /* Data frame styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def create_header(title, subtitle=None, icon="🏦"):
    """Create a consistent header for all pages"""
    st.markdown(f"""
    <div class="main-header">
        <h1>{icon} {title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def create_section_header(title, icon="📋"):
    """Create a section header with consistent styling"""
    st.markdown(f"""
    <div class="section-header">
        <h3>{icon} {title}</h3>
    </div>
    """, unsafe_allow_html=True)

def create_info_box(message, box_type="info"):
    """Create styled info boxes"""
    box_class = f"{box_type}-box"
    st.markdown(f"""
    <div class="{box_class}">
        {message}
    </div>
    """, unsafe_allow_html=True)

def create_persona_card(persona_data, is_selected=False):
    """Create a standardized persona card"""
    persona = persona_data.get('persona', {})
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
            <span class="persona-tag">💰 {income}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, icon="📊"):
    """Create a styled metric card"""
    st.markdown(f"""
    <div class="metric-container">
        <h4>{icon} {title}</h4>
        <p style="font-size: 1.5rem; font-weight: 600; color: #1f77b4; margin: 0;">{value}</p>
    </div>
    """, unsafe_allow_html=True)