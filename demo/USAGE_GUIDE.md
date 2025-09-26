# 🏦 Swiss Banking Persona Generator & Lifecycle Visualizer

## 🎉 Complete System Overview

You now have a comprehensive Swiss banking client persona generation and visualization system with the following capabilities:

### ✅ What's Been Built

1. **🎭 Enhanced Persona Generation**
   - 100+ realistic personas based on 71,458 real Swiss demographic records
   - Accurate age, income, regional, and cultural distributions
   - Swiss-specific banking context and preferences

2. **📈 Lifecycle Modeling**
   - Complete financial trajectories from birth to death (age 0-83)
   - Swiss 3-pillar pension system integration
   - Life stage transitions and financial milestones
   - Regional cost-of-living adjustments

3. **📊 Interactive Streamlit Dashboard** 
   - Real-time persona visualization and analytics
   - Lifecycle trajectory charts and projections
   - Interactive persona generation with custom parameters
   - Comprehensive demographic analysis

4. **🛠️ Flexible Generation Tools**
   - Command-line persona generators
   - Batch processing for large datasets
   - Custom prompt system for targeted generation

## 🚀 How to Use

### Launch the Streamlit App
```bash
cd demo
uv run streamlit run persona_visualizer_app.py
```
**App URL:** http://localhost:8501

### App Features

#### 📊 Demographics Overview
- Age and income distributions
- Regional representation 
- Gender balance analysis
- Education level breakdown

#### 📈 Lifecycle Analysis
- Individual persona financial trajectories
- Income, expenses, and asset growth over lifetime
- Financial milestones (first 100k, retirement readiness)
- Swiss pension system projections

#### 🎭 Generate New Personas
**Interactive parameters:**
- **Count:** 1-50 personas
- **Age Focus:** Young (20-35), Mid-career (35-50), Senior (50-65), All ages
- **Regional Focus:** Zürich, Bern, Basel, Geneva, Lausanne, All regions
- **Income Focus:** Low (30k-60k), Medium (60k-100k), High (100k+), All ranges
- **Risk Preference:** Conservative, Moderate, Aggressive, All types
- **Lifecycle Analysis:** Include/exclude detailed projections

#### 📋 Batch Analysis
- Aggregate analysis across all personas
- Retirement readiness distribution
- Average trajectory comparisons
- Population-level insights

### Command Line Tools

#### Generate Specific Personas
```bash
# Generate 20 enhanced personas
uv run python generate_personas.py --count 20 --output MY_CLIENTS

# Generate 5 Zürich-focused personas  
uv run python prompt.py prompts/enhanced_demo.md --examples 5 --output ZURICH_CLIENTS
```

#### Analyze Demographics
```bash
# Re-analyze the 71k Swiss demographic dataset
uv run python analyze_demographics.py
```

#### Add Lifecycle Data
```bash
# Enhance existing personas with lifecycle projections
uv run python persona_lifecycle.py
```

## 📁 File Structure

```
demo/
├── 🚀 MAIN APPS
│   ├── persona_visualizer_app.py    # Main Streamlit dashboard
│   └── streamlit.py                 # Original Streamlit (fallback)
│
├── 🎭 GENERATION TOOLS  
│   ├── generate_personas.py         # Easy persona generator
│   ├── generate_large_dataset.py    # Batch generator (100+ personas)
│   └── prompt.py                    # Generic prompt system
│
├── 📊 ANALYSIS & MODELING
│   ├── analyze_demographics.py      # Swiss demographic analyzer
│   └── persona_lifecycle.py         # Lifecycle modeling engine
│
├── 📝 PROMPTS
│   ├── prompts/demo.md             # Basic persona prompt
│   └── prompts/enhanced_demo.md    # Enhanced with demographics
│
└── 📦 DATA FILES
    ├── personas_dataset_100.json   # 100-persona master dataset
    ├── demographic_analysis.json   # Swiss demographic insights
    └── *_PERSONAS_*.json          # Generated persona collections
```

## 🎯 Key Features Delivered

### 1. Real Swiss Demographics Integration
- **71,458 records analyzed** for authentic patterns
- **Accurate distributions:** Age (avg 51.8), Income (CHF 89k avg), Regional (Zürich 18.6%)
- **Cultural context:** Swiss banking preferences, 3-pillar pension system

### 2. Complete Lifecycle Modeling
- **Birth to death projections** (age 0-83.8 years)
- **Financial milestones:** Emergency fund, first 100k, millionaire status
- **Life events:** Marriage, children, home purchase, career advancement
- **Retirement planning:** Asset projections, income replacement ratios

### 3. Interactive Visualization
- **Real-time charts** with Plotly integration
- **Persona comparison** and demographic breakdowns  
- **Lifecycle trajectories** with current age markers
- **Custom generation** with parameter controls

### 4. Flexible and Extensible
- **Modular design** for easy customization
- **Command-line tools** for automation
- **Custom prompts** for specific use cases
- **Batch processing** for large datasets

## 📊 Example Personas Generated

```json
{
  "name": "Hans-Jörg Müller",
  "age": 41,
  "profession": "Software Engineer",
  "annual_income": 85000,
  "current_assets": 500000,
  "family_status": "Verheiratet",
  "location": "Zürich",
  "language_region": "German", 
  "education_level": "Tertiary Level",
  "banking_preferences": ["Secure online banking", "Pension planning"],
  "lifecycle": {
    "projected_life_expectancy": 83.8,
    "retirement_projections": {
      "retirement_age": 65,
      "projected_retirement_assets": 2400000,
      "monthly_retirement_income": 8000
    }
  }
}
```

## 🎨 Customization Examples

### Custom Age-Focused Generation
```bash
uv run python generate_personas.py --count 15 --output YOUNG_PROFESSIONALS
# Then use age focus "Young (20-35)" in Streamlit
```

### Regional Banking Analysis  
```bash
uv run python generate_personas.py --count 25 --output GENEVA_CLIENTS
# Then use regional focus "Geneva" in Streamlit
```

### High-Net-Worth Clients
```bash
uv run python generate_personas.py --count 10 --output HNW_CLIENTS  
# Then use income focus "High (100k+)" in Streamlit
```

## 🔄 Typical Workflow

1. **Launch Dashboard:** `uv run streamlit run persona_visualizer_app.py`
2. **View Demographics:** Explore existing 100+ personas
3. **Analyze Lifecycles:** Select personas for detailed trajectory analysis
4. **Generate Custom:** Create targeted personas with specific parameters
5. **Batch Analysis:** Compare aggregate patterns and retirement readiness
6. **Export Data:** Save custom generations for further use

## 🎯 Use Cases

- **🏦 Banking App Testing:** Realistic Swiss client profiles
- **📊 Market Research:** Swiss demographic analysis and projections  
- **🎓 Training Data:** ML model training with authentic personas
- **💼 Product Development:** Client journey mapping and validation
- **📈 Financial Planning:** Retirement and lifecycle analysis tools
- **🎪 Demos & Presentations:** Compelling realistic client scenarios

Your system is now ready for comprehensive Swiss banking client simulation with both individual and population-level insights! 🎉