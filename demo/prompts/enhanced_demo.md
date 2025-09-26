# Enhanced Banking Client Personas with Swiss Demographic Data

## System Prompt
You are a helpful assistant that creates realistic banking client personas based on real Swiss demographic data. Always respond with valid JSON format. Use the provided demographic patterns to ensure your personas reflect actual Swiss population distributions.

## User Prompt
Create exactly 20 diverse banking client personas for a banking client simulation based on real Swiss demographic data.

## Demographic Context for Swiss Banking Client Personas

Based on analysis of 71,458 real Swiss demographic records, use the following patterns to create realistic personas:

### Age Distribution
- Average age: 51.8 years
- Age range: 15-100 years
- Most common age groups: 25-40 (working age), 45-65 (established professionals)

### Gender Distribution
- Female: 53.5%
- Male: 46.5%

### Family Status Distribution
- Verheiratet (Married): 53.2% of population
- Ledig (Single): 25.2% of population
- Geschieden (Divorced): 11.0% of population
- Verwitwet (Widowed): 8.9% of population
- Gerichtlich getrennt (Separated): 1.3% of population

### Regional Distribution (Top Cantons)
- Zürich: 18.6% (financial hub, higher incomes)
- Bern: 11.0% (government center)
- Waadt: 9.0% (Lausanne region)
- Luzern: 8.2%
- Aargau: 7.5%
- Tessin: 5.7%
- St. Gallen: 5.6%
- Genf: 5.3% (international banking)

### Language Regions
- German-speaking: 71.2%
- French-speaking: 22.9%
- Italian-speaking: 5.8%
- Romansh-speaking: 0.2%

### Education Levels
- Secondary Level II: 48.0% (apprenticeships, vocational training)
- Tertiary Level: 31.0% (universities, higher education)
- Secondary Level I: 21.0% (basic education)

### Employment Status
- Employees (Arbeitnehmer): 48.7%
- Retirees (Rentner): 28.2%
- Self-employed (Selbständige): 8.9%
- Homemakers: 3.5%
- Students: 2.6%
- Unemployed: 2.6%
- Other non-working: 2.4%

### Income Information
- Average annual income: CHF 89,147
- Median annual income: CHF 78,000
- Income range (25th-75th percentile): CHF 60,000 - CHF 108,000

### Swiss Banking Context
Consider these factors for realistic banking preferences:
- Swiss preference for financial privacy and security
- High adoption of digital banking (especially among younger demographics)
- Conservative investment approach but interest in sustainable investments
- Importance of pension planning (3-pillar system)
- Regional preferences (e.g., Zurich/Geneva for international banking, rural areas for traditional banking)

Each persona should include:
- name (realistic Swiss first and last name appropriate to language region)
- age (following demographic distribution)
- profession (realistic for Swiss job market and education level)
- annual_income (numeric value in CHF only, no text or comments)
- financial_goals (array of goals appropriate to age and life situation)
- risk_tolerance (low, medium, high - consider Swiss conservative tendencies)
- current_assets (numeric value in CHF only, no text or comments)
- monthly_expenses (numeric value in CHF only, no text or comments)
- family_status (following demographic distribution)
- location (Swiss city/canton following demographic distribution)
- language_region (German/French/Italian/Romansh following distribution)
- education_level (following demographic distribution)
- banking_preferences (array reflecting Swiss banking culture and demographics)

IMPORTANT: Return ONLY valid JSON format. Use only numeric values for income, assets, and expenses. No comments or explanatory text in the JSON values.

Return as a JSON object with a 'personas' array containing all 20 personas. Ensure demographic realism based on the provided Swiss data patterns.