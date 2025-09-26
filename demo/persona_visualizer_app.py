import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np
from datetime import datetime
import subprocess
import sys
import tempfile
import os
from pathlib import Path

# Import our custom modules
from persona_lifecycle import PersonaLifecycleModel, enhance_personas_with_lifecycle

# Page configuration
st.set_page_config(
    page_title="Swiss Banking Persona Generator & Lifecycle Visualizer",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .persona-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class PersonaVisualizerApp:
    def __init__(self):
        self.lifecycle_model = PersonaLifecycleModel()
        
    def load_personas_data(self, file_path: str = None):
        """Load personas data from file or use default."""
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Try to find existing persona files
        import glob
        persona_files = glob.glob("*PERSONAS*.json") + glob.glob("personas_dataset*.json")
        
        if persona_files:
            latest_file = max(persona_files, key=lambda f: os.path.getctime(f))
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {"personas": []}
    
    def create_demographics_overview(self, personas):
        """Create demographic overview charts."""
        df = pd.DataFrame(personas)
        
        if df.empty:
            st.warning("No personas data available")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_age = df['age'].mean()
            st.metric("Average Age", f"{avg_age:.1f} years")
        
        with col2:
            avg_income = df['annual_income'].mean()
            st.metric("Average Income", f"CHF {avg_income:,.0f}")
        
        with col3:
            female_pct = (df['gender'].str.lower() == 'female').mean() * 100 if 'gender' in df.columns else 0
            st.metric("Female %", f"{female_pct:.1f}%")
        
        with col4:
            total_personas = len(df)
            st.metric("Total Personas", total_personas)
        
        # Age distribution
        fig_age = px.histogram(df, x='age', nbins=20, title="Age Distribution")
        st.plotly_chart(fig_age, use_container_width=True)
        
        # Income vs Age
        fig_income = px.scatter(df, x='age', y='annual_income', 
                              title="Income vs Age", 
                              hover_data=['name', 'profession'] if 'name' in df.columns else None)
        st.plotly_chart(fig_income, use_container_width=True)
        
        # Regional distribution
        if 'location' in df.columns:
            location_counts = df['location'].value_counts()
            fig_location = px.pie(values=location_counts.values, names=location_counts.index,
                                title="Regional Distribution")
            st.plotly_chart(fig_location, use_container_width=True)
    
    def create_lifecycle_visualization(self, personas):
        """Create lifecycle visualization charts."""
        st.subheader("📈 Lifecycle Analysis")
        
        if not personas:
            st.warning("No personas available for lifecycle analysis")
            return
        
        # Select persona for detailed lifecycle view
        persona_names = [p.get('name', f"Persona {i}") for i, p in enumerate(personas)]
        selected_persona_name = st.selectbox("Select persona for detailed lifecycle:", persona_names)
        
        if selected_persona_name:
            selected_idx = persona_names.index(selected_persona_name)
            selected_persona = personas[selected_idx]
            
            # Generate lifecycle if not present
            if 'lifecycle' not in selected_persona:
                with st.spinner("Generating lifecycle data..."):
                    lifecycle_data = self.lifecycle_model.calculate_lifecycle_trajectory(selected_persona)
                    selected_persona['lifecycle'] = lifecycle_data
            
            self.display_persona_lifecycle(selected_persona)
    
    def display_persona_lifecycle(self, persona):
        """Display detailed lifecycle for a single persona."""
        lifecycle = persona.get('lifecycle', {})
        trajectory = lifecycle.get('annual_trajectory', [])
        
        if not trajectory:
            st.error("No lifecycle data available")
            return
        
        # Persona summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **{persona.get('name', 'Unknown')}**
            - Age: {persona.get('age')} years
            - Profession: {persona.get('profession', 'Unknown')}
            - Location: {persona.get('location', 'Unknown')}
            """)
        
        with col2:
            st.markdown(f"""
            **Financial Status**
            - Annual Income: CHF {persona.get('annual_income', 0):,}
            - Current Assets: CHF {persona.get('current_assets', 0):,}
            - Risk Tolerance: {persona.get('risk_tolerance', 'Unknown')}
            """)
        
        with col3:
            retirement_proj = lifecycle.get('retirement_projections', {})
            st.markdown(f"""
            **Retirement Outlook**
            - Years to Retirement: {retirement_proj.get('years_to_retirement', 'N/A')}
            - Projected Assets: CHF {retirement_proj.get('projected_retirement_assets', 0):,}
            - Monthly Retirement Income: CHF {retirement_proj.get('monthly_retirement_income', 0):,}
            """)
        
        # Lifecycle charts
        df_trajectory = pd.DataFrame(trajectory)
        
        # Income and expenses over time
        fig_income = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Annual Income & Expenses Over Lifetime', 'Cumulative Assets Growth'),
            vertical_spacing=0.1
        )
        
        fig_income.add_trace(
            go.Scatter(x=df_trajectory['age'], y=df_trajectory['annual_income'], 
                      name='Annual Income', line=dict(color='green')),
            row=1, col=1
        )
        
        fig_income.add_trace(
            go.Scatter(x=df_trajectory['age'], y=df_trajectory['annual_expenses'], 
                      name='Annual Expenses', line=dict(color='red')),
            row=1, col=1
        )
        
        fig_income.add_trace(
            go.Scatter(x=df_trajectory['age'], y=df_trajectory['cumulative_assets'], 
                      name='Cumulative Assets', line=dict(color='blue')),
            row=2, col=1
        )
        
        # Add current age marker
        current_age = persona.get('age', 0)
        fig_income.add_vline(x=current_age, line_dash="dash", line_color="orange",
                           annotation_text="Current Age")
        
        fig_income.update_layout(height=600, showlegend=True)
        fig_income.update_xaxes(title_text="Age", row=2, col=1)
        fig_income.update_yaxes(title_text="CHF", row=1, col=1)
        fig_income.update_yaxes(title_text="CHF", row=2, col=1)
        
        st.plotly_chart(fig_income, use_container_width=True)
        
        # Life stages visualization
        life_stages = df_trajectory['life_stage'].value_counts()
        fig_stages = px.pie(values=life_stages.values, names=life_stages.index,
                           title="Time Spent in Life Stages")
        st.plotly_chart(fig_stages, use_container_width=True)
        
        # Financial milestones
        milestones = lifecycle.get('life_milestones', [])
        if milestones:
            st.subheader("🎯 Financial Milestones")
            milestone_df = pd.DataFrame(milestones)
            
            fig_milestones = px.scatter(milestone_df, x='age', y='value', 
                                      text='milestone', size='value',
                                      title="Financial Milestones Timeline")
            fig_milestones.update_traces(textposition="top center")
            st.plotly_chart(fig_milestones, use_container_width=True)
    
    def create_batch_lifecycle_analysis(self, personas):
        """Create aggregate lifecycle analysis for all personas."""
        st.subheader("📊 Batch Lifecycle Analysis")
        
        if len(personas) < 2:
            st.warning("Need at least 2 personas for batch analysis")
            return
        
        # Generate lifecycle data for all personas
        enhanced_personas = []
        progress_bar = st.progress(0)
        
        for i, persona in enumerate(personas):
            if 'lifecycle' not in persona:
                lifecycle_data = self.lifecycle_model.calculate_lifecycle_trajectory(persona)
                persona['lifecycle'] = lifecycle_data
            enhanced_personas.append(persona)
            progress_bar.progress((i + 1) / len(personas))
        
        # Aggregate analysis
        self.create_aggregate_charts(enhanced_personas)
    
    def create_aggregate_charts(self, personas):
        """Create aggregate visualization charts."""
        
        # Retirement readiness analysis
        retirement_data = []
        for persona in personas:
            retirement_proj = persona.get('lifecycle', {}).get('retirement_projections', {})
            retirement_data.append({
                'name': persona.get('name', 'Unknown'),
                'current_age': persona.get('age', 0),
                'projected_assets': retirement_proj.get('projected_retirement_assets', 0),
                'replacement_ratio': retirement_proj.get('income_replacement_ratio', 0),
                'years_to_retirement': retirement_proj.get('years_to_retirement', 0)
            })
        
        retirement_df = pd.DataFrame(retirement_data)
        
        # Retirement assets distribution
        fig_retirement = px.histogram(retirement_df, x='projected_assets', nbins=20,
                                    title="Distribution of Projected Retirement Assets")
        st.plotly_chart(fig_retirement, use_container_width=True)
        
        # Income replacement ratio
        fig_replacement = px.scatter(retirement_df, x='current_age', y='replacement_ratio',
                                   title="Income Replacement Ratio by Current Age",
                                   hover_data=['name'])
        st.plotly_chart(fig_replacement, use_container_width=True)
        
        # Average trajectory by age group
        age_groups = ['25-35', '35-45', '45-55', '55-65']
        trajectory_data = []
        
        for persona in personas:
            trajectory = persona.get('lifecycle', {}).get('annual_trajectory', [])
            for year_data in trajectory:
                age = year_data.get('age', 0)
                if 25 <= age <= 65:
                    age_group = f"{(age//10)*10}-{(age//10)*10+10}"
                    trajectory_data.append({
                        'age': age,
                        'age_group': age_group,
                        'income': year_data.get('annual_income', 0),
                        'assets': year_data.get('cumulative_assets', 0),
                        'expenses': year_data.get('annual_expenses', 0)
                    })
        
        if trajectory_data:
            traj_df = pd.DataFrame(trajectory_data)
            
            # Average income by age
            avg_income = traj_df.groupby('age')['income'].mean().reset_index()
            fig_avg_income = px.line(avg_income, x='age', y='income',
                                   title="Average Income Trajectory Across All Personas")
            st.plotly_chart(fig_avg_income, use_container_width=True)
    
    def create_persona_generator_interface(self):
        """Create interactive persona generation interface."""
        st.subheader("🎭 Generate New Personas")
        
        with st.form("persona_generator"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                count = st.slider("Number of personas", 1, 50, 10)
                age_range = st.select_slider(
                    "Age focus",
                    options=["Young (20-35)", "Mid-career (35-50)", "Senior (50-65)", "All ages"],
                    value="All ages"
                )
            
            with col2:
                regions = ["All regions", "Zürich", "Bern", "Basel", "Geneva", "Lausanne"]
                region_focus = st.selectbox("Regional focus", regions)
                
                income_range = st.select_slider(
                    "Income focus",
                    options=["Low (30k-60k)", "Medium (60k-100k)", "High (100k+)", "All ranges"],
                    value="All ranges"
                )
            
            with col3:
                risk_preference = st.selectbox(
                    "Risk tolerance focus",
                    ["All types", "Conservative (low)", "Moderate (medium)", "Aggressive (high)"]
                )
                
                include_lifecycle = st.checkbox("Include lifecycle analysis", value=True)
            
            submit_button = st.form_submit_button("🚀 Generate Personas")
            
            if submit_button:
                self.generate_custom_personas(count, age_range, region_focus, 
                                            income_range, risk_preference, include_lifecycle)
    
    def generate_custom_personas(self, count, age_range, region_focus, income_range, risk_preference, include_lifecycle):
        """Generate personas with custom parameters."""
        
        with st.spinner(f"Generating {count} custom personas..."):
            # Create custom prompt based on parameters
            custom_prompt = self.create_custom_prompt(count, age_range, region_focus, 
                                                    income_range, risk_preference)
            
            # Save custom prompt to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(custom_prompt)
                temp_prompt_file = f.name
            
            try:
                # Generate personas using our prompt system
                result = subprocess.run([
                    sys.executable, "prompt.py",
                    temp_prompt_file,
                    "--examples", str(count),
                    "--output", "CUSTOM_GENERATED"
                ], capture_output=True, text=True, cwd=".")
                
                if result.returncode == 0:
                    # Find the generated file
                    import glob
                    custom_files = glob.glob("CUSTOM_GENERATED-*.json")
                    if custom_files:
                        latest_file = max(custom_files, key=lambda f: os.path.getctime(f))
                        
                        # Load and display generated personas
                        with open(latest_file, 'r', encoding='utf-8') as f:
                            generated_data = json.load(f)
                        
                        personas = generated_data.get('personas', [])
                        
                        if include_lifecycle and personas:
                            # Add lifecycle data
                            for persona in personas:
                                lifecycle_data = self.lifecycle_model.calculate_lifecycle_trajectory(persona)
                                persona['lifecycle'] = lifecycle_data
                        
                        st.success(f"✅ Generated {len(personas)} personas successfully!")
                        
                        # Display generated personas
                        self.display_generated_personas(personas)
                        
                        # Option to save
                        if st.button("💾 Save Generated Personas"):
                            save_filename = f"custom_personas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                            with open(save_filename, 'w', encoding='utf-8') as f:
                                json.dump({"personas": personas}, f, indent=2, ensure_ascii=False)
                            st.success(f"Saved to {save_filename}")
                    else:
                        st.error("No output file generated")
                else:
                    st.error(f"Generation failed: {result.stderr}")
                    
            finally:
                # Clean up temporary file
                os.unlink(temp_prompt_file)
    
    def create_custom_prompt(self, count, age_range, region_focus, income_range, risk_preference):
        """Create custom prompt based on parameters."""
        
        # Base prompt
        prompt = f"""# Custom Swiss Banking Personas

## System Prompt
You are a helpful assistant that creates realistic Swiss banking client personas. Always respond with valid JSON format.

## User Prompt
Create exactly {count} diverse Swiss banking client personas with the following specifications:

"""
        
        # Add parameter-specific instructions
        if age_range != "All ages":
            if "Young" in age_range:
                prompt += "- Focus on ages 20-35 (early career, starting families)\n"
            elif "Mid-career" in age_range:
                prompt += "- Focus on ages 35-50 (career growth, family responsibilities)\n"
            elif "Senior" in age_range:
                prompt += "- Focus on ages 50-65 (peak career, retirement planning)\n"
        
        if region_focus != "All regions":
            prompt += f"- Geographic focus: {region_focus} region\n"
        
        if income_range != "All ranges":
            if "Low" in income_range:
                prompt += "- Income range: CHF 30,000-60,000\n"
            elif "Medium" in income_range:
                prompt += "- Income range: CHF 60,000-100,000\n"
            elif "High" in income_range:
                prompt += "- Income range: CHF 100,000+\n"
        
        if risk_preference != "All types":
            if "Conservative" in risk_preference:
                prompt += "- Risk tolerance: Primarily low risk tolerance\n"
            elif "Moderate" in risk_preference:
                prompt += "- Risk tolerance: Primarily medium risk tolerance\n"
            elif "Aggressive" in risk_preference:
                prompt += "- Risk tolerance: Primarily high risk tolerance\n"
        
        # Standard persona structure
        prompt += """
Each persona should include:
- name (realistic Swiss name)
- age
- profession
- annual_income (in CHF)
- financial_goals (array)
- risk_tolerance (low, medium, high)
- current_assets (in CHF)
- monthly_expenses (in CHF)
- family_status
- location (Swiss city)
- language_region
- education_level
- banking_preferences (array)

Return as JSON with 'personas' array. Use only numeric values for financial fields.
"""
        
        return prompt
    
    def display_generated_personas(self, personas):
        """Display generated personas in cards."""
        st.subheader("Generated Personas")
        
        for i, persona in enumerate(personas):
            with st.expander(f"👤 {persona.get('name', f'Persona {i+1}')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Age:** {persona.get('age')}")
                    st.write(f"**Profession:** {persona.get('profession')}")
                    st.write(f"**Location:** {persona.get('location')}")
                
                with col2:
                    st.write(f"**Annual Income:** CHF {persona.get('annual_income', 0):,}")
                    st.write(f"**Current Assets:** CHF {persona.get('current_assets', 0):,}")
                    st.write(f"**Risk Tolerance:** {persona.get('risk_tolerance')}")
                
                with col3:
                    st.write(f"**Family Status:** {persona.get('family_status')}")
                    st.write(f"**Education:** {persona.get('education_level')}")
                    goals = persona.get('financial_goals', [])
                    st.write(f"**Goals:** {', '.join(goals[:2]) if goals else 'None listed'}")
    
    def run(self):
        """Main app runner."""
        st.markdown('<h1 class="main-header">🏦 Swiss Banking Persona Generator & Lifecycle Visualizer</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Choose a view:",
            ["📊 Demographics Overview", "📈 Lifecycle Analysis", "🎭 Generate New Personas", "📋 Batch Analysis"]
        )
        
        # Load data
        data = self.load_personas_data()
        personas = data.get('personas', [])
        
        if not personas:
            st.warning("⚠️ No personas data found. Generate some personas first!")
            self.create_persona_generator_interface()
            return
        
        st.sidebar.success(f"✅ Loaded {len(personas)} personas")
        
        # Main content based on selection
        if page == "📊 Demographics Overview":
            st.header("Demographics Overview")
            self.create_demographics_overview(personas)
            
        elif page == "📈 Lifecycle Analysis":
            self.create_lifecycle_visualization(personas)
            
        elif page == "🎭 Generate New Personas":
            self.create_persona_generator_interface()
            
        elif page == "📋 Batch Analysis":
            if len(personas) >= 5:
                self.create_batch_lifecycle_analysis(personas)
            else:
                st.warning("Need at least 5 personas for meaningful batch analysis")

def main():
    app = PersonaVisualizerApp()
    app.run()

if __name__ == "__main__":
    main()