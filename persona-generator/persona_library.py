import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def load_saved_batches():
    """Load all saved persona batches from the generated_personas directory"""
    personas_dir = Path(__file__).parent / "generated_personas"
    
    if not personas_dir.exists():
        return []
    
    batches = []
    for file_path in personas_dir.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
            
            # Add file info to metadata
            batch_data['metadata']['filepath'] = str(file_path)
            batch_data['metadata']['filename'] = file_path.name
            batches.append(batch_data)
        except Exception as e:
            st.error(f"Error loading {file_path.name}: {str(e)}")
    
    # Sort by generation date (newest first)
    batches.sort(key=lambda x: x['metadata'].get('generated_at', ''), reverse=True)
    return batches

def create_personas_dataframe(personas):
    """Convert personas to a pandas DataFrame for analysis"""
    data = []
    
    for i, p in enumerate(personas):
        persona = p['persona']
        source_data = p.get('source_data', {})
        
        # Extract key fields
        basic_info = persona.get('basic_info', {})
        demographics = persona.get('demographics', {})
        professional = persona.get('professional', {})
        financial = persona.get('financial', {})
        banking_persona = persona.get('banking_persona', {})
        banking_prefs = banking_persona.get('banking_preferences', {})
        personality = persona.get('personality', {})
        
        row = {
            'ID': persona.get('persona_id', f'P_{i+1}'),
            'Name': basic_info.get('name', ''),
            'Age': basic_info.get('age', ''),
            'Gender': basic_info.get('gender', ''),
            'Canton': demographics.get('canton', ''),
            'Region': demographics.get('region', ''),
            'Household_Size': demographics.get('household_size', ''),
            'Marital_Status': demographics.get('marital_status', ''),
            'Children': demographics.get('children', ''),
            'Housing': demographics.get('housing', ''),
            'Job_Title': professional.get('job_title', ''),
            'Industry': professional.get('industry', ''),
            'Employment_Status': professional.get('employment_status', ''),
            'Income_CHF': financial.get('annual_gross_income_chf', ''),
            'Disposable_Income': financial.get('disposable_income_category', ''),
            'Net_Worth': financial.get('net_worth_category', ''),
            'Financial_Experience': financial.get('financial_experience', ''),
            'Risk_Tolerance': banking_persona.get('risk_tolerance', ''),
            'Investment_Interest': banking_persona.get('investment_interest', ''),
            'Channel_Preference': banking_prefs.get('channel_preference', ''),
            'Service_Level': banking_prefs.get('service_level', ''),
            'Product_Complexity': banking_prefs.get('product_complexity', ''),
            'Banking_Frequency': banking_persona.get('banking_frequency', ''),
            'Technology_Affinity': personality.get('technology_affinity', ''),
            'Decision_Making_Style': personality.get('decision_making_style', '')
        }
        
        data.append(row)
    
    return pd.DataFrame(data)

def create_demographics_charts(df):
    """Create demographic analysis charts"""
    charts = {}
    
    # Age distribution
    if 'Age' in df.columns and df['Age'].notna().any():
        fig_age = px.histogram(df, x='Age', title='Age Distribution', 
                              nbins=20, color_discrete_sequence=['#1f77b4'])
        charts['age'] = fig_age
    
    # Gender distribution
    if 'Gender' in df.columns and df['Gender'].notna().any():
        gender_counts = df['Gender'].value_counts()
        fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index, 
                           title='Gender Distribution')
        charts['gender'] = fig_gender
    
    # Canton distribution (top 10)
    if 'Canton' in df.columns and df['Canton'].notna().any():
        canton_counts = df['Canton'].value_counts().head(10)
        fig_canton = px.bar(x=canton_counts.index, y=canton_counts.values, 
                           title='Top 10 Cantons', labels={'x': 'Canton', 'y': 'Count'})
        charts['canton'] = fig_canton
    
    # Income distribution
    if 'Income_CHF' in df.columns and df['Income_CHF'].notna().any():
        # Convert to numeric, handle non-numeric values
        numeric_income = pd.to_numeric(df['Income_CHF'], errors='coerce').dropna()
        if len(numeric_income) > 0:
            fig_income = px.histogram(numeric_income, title='Income Distribution (CHF)', 
                                    nbins=20, color_discrete_sequence=['#2ca02c'])
            charts['income'] = fig_income
    
    return charts

def create_banking_charts(df):
    """Create banking behavior analysis charts"""
    charts = {}
    
    # Risk tolerance
    if 'Risk_Tolerance' in df.columns and df['Risk_Tolerance'].notna().any():
        risk_counts = df['Risk_Tolerance'].value_counts()
        fig_risk = px.pie(values=risk_counts.values, names=risk_counts.index, 
                         title='Risk Tolerance Distribution')
        charts['risk'] = fig_risk
    
    # Channel preference
    if 'Channel_Preference' in df.columns and df['Channel_Preference'].notna().any():
        channel_counts = df['Channel_Preference'].value_counts()
        fig_channel = px.bar(x=channel_counts.values, y=channel_counts.index, 
                            orientation='h', title='Channel Preferences')
        charts['channel'] = fig_channel
    
    # Investment interest vs Risk tolerance
    if all(col in df.columns for col in ['Investment_Interest', 'Risk_Tolerance']):
        crosstab = pd.crosstab(df['Investment_Interest'], df['Risk_Tolerance'])
        if not crosstab.empty:
            fig_cross = px.imshow(crosstab, text_auto=True, 
                                 title='Investment Interest vs Risk Tolerance')
            charts['investment_risk'] = fig_cross
    
    return charts

def show():
    """Show the persona library page"""
    
    st.title("📚 Persona Library")
    st.write("Browse, analyze, and manage your generated banking personas.")
    
    # Load saved batches
    batches = load_saved_batches()
    
    if not batches:
        st.info("No saved persona batches found. Generate some personas first using the Batch Generation page!")
        return
    
    # Batch selection
    st.write("### Saved Batches")
    
    # Create batch options for selectbox
    batch_options = []
    for i, batch in enumerate(batches):
        metadata = batch['metadata']
        generated_at = datetime.fromisoformat(metadata['generated_at']).strftime("%Y-%m-%d %H:%M")
        total_personas = metadata['total_personas']
        batch_id = metadata['batch_id'][:8]
        
        batch_options.append({
            'label': f"{generated_at} | {total_personas} personas | ID: {batch_id}",
            'index': i,
            'batch': batch
        })
    
    selected_batch_idx = st.selectbox(
        "Select a batch to explore:",
        range(len(batch_options)),
        format_func=lambda x: batch_options[x]['label']
    )
    
    if selected_batch_idx is not None:
        selected_batch = batch_options[selected_batch_idx]['batch']
        personas = selected_batch['personas']
        metadata = selected_batch['metadata']
        
        # Batch info
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        with col_info1:
            st.metric("Total Personas", metadata['total_personas'])
        with col_info2:
            generated_date = datetime.fromisoformat(metadata['generated_at']).strftime("%Y-%m-%d")
            st.metric("Generated", generated_date)
        with col_info3:
            st.metric("Batch ID", metadata['batch_id'][:8])
        with col_info4:
            if st.button("🗑️ Delete Batch", help="Delete this batch file"):
                try:
                    Path(metadata['filepath']).unlink()
                    st.success("Batch deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting batch: {str(e)}")
        
        # Create tabs for different views
        tab_browse, tab_analytics, tab_export = st.tabs(["🔍 Browse Personas", "📊 Analytics", "💾 Export"])
        
        with tab_browse:
            st.write("### Individual Personas")
            
            # Convert to DataFrame for easier handling
            df = create_personas_dataframe(personas)
            
            # Persona selector
            if not df.empty:
                # Add search/filter
                search_term = st.text_input("🔍 Search personas (by name, job, canton...):", "")
                
                # Filter DataFrame based on search
                if search_term:
                    mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                    filtered_df = df[mask]
                else:
                    filtered_df = df
                
                if not filtered_df.empty:
                    # Persona selection
                    selected_persona_idx = st.selectbox(
                        f"Select persona ({len(filtered_df)} found):",
                        range(len(filtered_df)),
                        format_func=lambda x: f"{filtered_df.iloc[x]['Name']} | {filtered_df.iloc[x]['Age']} | {filtered_df.iloc[x]['Canton']}"
                    )
                    
                    if selected_persona_idx is not None:
                        # Find original index in the personas list
                        original_idx = filtered_df.index[selected_persona_idx]
                        selected_persona_data = personas[original_idx]
                        selected_persona = selected_persona_data['persona']
                        
                        # Display persona details
                        col_basic, col_banking = st.columns(2)
                        
                        with col_basic:
                            st.subheader("👤 Basic Information")
                            basic = selected_persona.get('basic_info', {})
                            demographics = selected_persona.get('demographics', {})
                            professional = selected_persona.get('professional', {})
                            
                            st.write(f"**Name:** {basic.get('name', 'N/A')}")
                            st.write(f"**Age:** {basic.get('age', 'N/A')}")
                            st.write(f"**Gender:** {basic.get('gender', 'N/A')}")
                            st.write(f"**Canton:** {demographics.get('canton', 'N/A')}")
                            st.write(f"**Marital Status:** {demographics.get('marital_status', 'N/A')}")
                            st.write(f"**Job:** {professional.get('job_title', 'N/A')}")
                            st.write(f"**Industry:** {professional.get('industry', 'N/A')}")
                        
                        with col_banking:
                            st.subheader("🏦 Banking Profile")
                            banking = selected_persona.get('banking_persona', {})
                            financial = selected_persona.get('financial', {})
                            prefs = banking.get('banking_preferences', {})
                            
                            st.write(f"**Income:** {financial.get('annual_gross_income_chf', 'N/A')} CHF")
                            st.write(f"**Net Worth:** {financial.get('net_worth_category', 'N/A')}")
                            st.write(f"**Risk Tolerance:** {banking.get('risk_tolerance', 'N/A')}")
                            st.write(f"**Investment Interest:** {banking.get('investment_interest', 'N/A')}")
                            st.write(f"**Channel Preference:** {prefs.get('channel_preference', 'N/A')}")
                            st.write(f"**Service Level:** {prefs.get('service_level', 'N/A')}")
                        
                        # Financial goals and narrative
                        if 'financial_goals' in banking:
                            st.subheader("🎯 Financial Goals")
                            for goal in banking['financial_goals']:
                                st.write(f"• {goal}")
                        
                        if 'narrative' in selected_persona:
                            st.subheader("📖 Life Story")
                            narrative = selected_persona['narrative']
                            st.write(f"**Background:** {narrative.get('life_story', 'N/A')}")
                        
                        # Full JSON
                        with st.expander("📄 View Full JSON"):
                            st.json(selected_persona)
                else:
                    st.warning("No personas match your search term.")
        
        with tab_analytics:
            st.write("### Batch Analytics")
            
            df = create_personas_dataframe(personas)
            
            if not df.empty:
                # Demographics section
                st.subheader("👥 Demographics")
                demo_charts = create_demographics_charts(df)
                
                if demo_charts:
                    chart_cols = st.columns(2)
                    chart_idx = 0
                    for chart_name, chart in demo_charts.items():
                        with chart_cols[chart_idx % 2]:
                            st.plotly_chart(chart, use_container_width=True)
                        chart_idx += 1
                
                # Banking behavior section
                st.subheader("🏦 Banking Behavior")
                banking_charts = create_banking_charts(df)
                
                if banking_charts:
                    chart_cols = st.columns(2)
                    chart_idx = 0
                    for chart_name, chart in banking_charts.items():
                        with chart_cols[chart_idx % 2]:
                            st.plotly_chart(chart, use_container_width=True)
                        chart_idx += 1
                
                # Summary statistics
                st.subheader("📈 Summary Statistics")
                
                # Numeric columns summary
                numeric_cols = ['Age', 'Income_CHF', 'Household_Size']
                for col in numeric_cols:
                    if col in df.columns:
                        numeric_data = pd.to_numeric(df[col], errors='coerce').dropna()
                        if len(numeric_data) > 0:
                            st.write(f"**{col}:**")
                            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                            with col_stats1:
                                st.metric("Mean", f"{numeric_data.mean():.1f}")
                            with col_stats2:
                                st.metric("Median", f"{numeric_data.median():.1f}")
                            with col_stats3:
                                st.metric("Min", f"{numeric_data.min():.1f}")
                            with col_stats4:
                                st.metric("Max", f"{numeric_data.max():.1f}")
        
        with tab_export:
            st.write("### Export Options")
            
            # Full JSON export
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                st.write("**Full Batch Export**")
                if st.button("💾 Download Complete Batch JSON"):
                    with open(metadata['filepath'], 'r', encoding='utf-8') as f:
                        batch_data = f.read()
                    
                    st.download_button(
                        label="Download Full Batch",
                        data=batch_data,
                        file_name=f"batch_{metadata['batch_id'][:8]}.json",
                        mime="application/json"
                    )
            
            with col_export2:
                st.write("**Summary CSV Export**")
                if st.button("📊 Download Personas CSV"):
                    df = create_personas_dataframe(personas)
                    csv_data = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV Summary",
                        data=csv_data,
                        file_name=f"personas_{metadata['batch_id'][:8]}.csv",
                        mime="text/csv"
                    )
            
            # Individual persona exports
            st.write("---")
            st.write("**Individual Persona Export**")
            
            persona_names = [p['persona'].get('basic_info', {}).get('name', f'Persona {i+1}') 
                           for i, p in enumerate(personas)]
            
            selected_export_idx = st.selectbox(
                "Select persona to export:",
                range(len(personas)),
                format_func=lambda x: persona_names[x]
            )
            
            if selected_export_idx is not None:
                selected_persona = personas[selected_export_idx]['persona']
                persona_json = json.dumps(selected_persona, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="Download Selected Persona JSON",
                    data=persona_json,
                    file_name=f"persona_{selected_persona.get('persona_id', 'unknown')}.json",
                    mime="application/json"
                )