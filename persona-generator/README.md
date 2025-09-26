# Banking Persona Generator - Multi-Page App

A comprehensive tool for generating realistic Swiss banking personas using AI and real demographic data.

## 🚀 **New Multi-Page Application**

The app now has three main pages accessible via the sidebar:

### 1. 👤 **Single Persona** 
*Generate one persona at a time with real-time feedback*

- **Demographic Filters**: Age groups, gender, canton, language region, income, education, employment status
- **Banking Parameters**: Net worth, disposable income, major expenses, housing, financial experience  
- **Real-time Generation**: Immediate feedback with debug mode available
- **Structured Display**: Organized view of persona data with JSON export

### 2. 🎯 **Batch Generation**
*Generate 1-100 personas at once with progress tracking*

#### **Key Features:**
- **Batch Size**: Generate up to 100 personas in one operation
- **Progress Tracking**: Real-time progress bar and status updates
- **Parameter Modes**:
  - **Fixed**: All personas share identical banking parameters
  - **Random**: Each persona gets randomly varied banking characteristics
- **Consistent Filters**: All personas follow the same demographic criteria
- **Auto-Save**: Generated batches automatically saved with timestamps
- **Export Options**: Full JSON batch file or CSV summary

#### **Use Cases:**
- Market research and customer segmentation
- Bulk test data for banking systems
- Demographic studies of specific populations
- Customer journey simulation datasets

### 3. 📚 **Persona Library**
*Browse, analyze, and manage your generated personas*

#### **Features:**
- **Batch Management**: View all saved persona batches with metadata
- **Search & Filter**: Find specific personas by name, job, canton, etc.
- **Individual Browse**: Detailed view of each persona with full data
- **Analytics Dashboard**: 
  - Demographics charts (age, gender, canton, income)
  - Banking behavior analysis (risk tolerance, channel preferences)
  - Cross-tabulation analysis (investment interest vs risk tolerance)
  - Summary statistics for numeric fields
- **Export Options**: 
  - Individual persona JSON files
  - Batch CSV summaries
  - Complete batch JSON files
- **Batch Deletion**: Remove unwanted batches

## 🔧 **Technical Features**

### **Data Storage:**
- Personas saved in `generated_personas/` directory
- JSON format with metadata and timestamps
- Batch IDs for unique identification

### **Analytics:**
- Plotly-powered interactive charts
- Demographic distribution analysis
- Banking behavior insights
- Cross-correlation studies

### **Error Handling:**
- Robust JSON parsing with auto-fix capabilities  
- Progress tracking with error reporting
- Graceful handling of generation failures

## 📊 **Generated Data Structure**

Each persona includes:
- **Basic Info**: Name, age, gender, nationality, languages
- **Demographics**: Canton, region, household info, housing
- **Professional**: Job, industry, employment status, income
- **Financial**: Income, net worth, expenses, experience level
- **Banking Profile**: Risk tolerance, investment interest, preferences
- **Personality**: Traits, values, lifestyle, technology affinity
- **Narrative**: Life story, current situation, future aspirations
- **Banking Scenarios**: Products, triggers, communication preferences

## 🎯 **Workflow Recommendations**

1. **Start with Single Persona**: Test filters and parameters
2. **Generate Small Batches**: Try 5-10 personas to validate settings
3. **Scale Up**: Generate larger batches (50-100) for analysis
4. **Use Library**: Analyze patterns and export data for further use

## 🚀 **Getting Started**

1. Run the app: `uv run streamlit run main_app.py`
2. Navigate to http://localhost:8502
3. Use the sidebar to switch between pages
4. Start with Single Persona to understand the system
5. Move to Batch Generation for bulk creation
6. Explore Persona Library for analysis and management

The system is now production-ready for comprehensive banking persona generation and analysis!