import pandas as pd
import numpy as np
from collections import Counter
import json

def analyze_demographic_data(csv_path):
    """Analyze the demographic data to extract patterns for persona generation."""
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    print(f"Total records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Basic statistics
    analysis = {
        "total_records": len(df),
        "age_distribution": {
            "mean": float(df['alter'].mean()),
            "median": float(df['alter'].median()),
            "min": int(df['alter'].min()),
            "max": int(df['alter'].max()),
            "quartiles": {
                "q1": float(df['alter'].quantile(0.25)),
                "q3": float(df['alter'].quantile(0.75))
            }
        },
        "gender_distribution": {
            "female_percentage": float((df['weiblich'] == 1).mean() * 100),
            "male_percentage": float((df['weiblich'] == 0).mean() * 100)
        },
        "family_status_distribution": dict(df['fam_status'].value_counts().to_dict()),
        "canton_distribution": dict(df['kanton'].value_counts().head(10).to_dict()),
        "language_region_distribution": dict(df['sprachgebiet'].value_counts().to_dict()),
        "education_levels": dict(df['bildungsniveau'].value_counts().to_dict()),
        "employment_status": dict(df['erwerbsstatus'].value_counts().to_dict()),
        "profession_categories": dict(df['beruf'].value_counts().head(15).to_dict()),
        "household_size_distribution": dict(df['hhgroesse'].value_counts().to_dict()),
        "children_distribution": {
            "with_children_percentage": float((df['kinder'] == 1).mean() * 100),
            "without_children_percentage": float((df['kinder'] == 0).mean() * 100)
        }
    }
    
    # Income analysis (handling NA values)
    income_data = df['bruttojahr'].dropna()
    if len(income_data) > 0:
        analysis["income_distribution"] = {
            "mean": float(income_data.mean()),
            "median": float(income_data.median()),
            "quartiles": {
                "q1": float(income_data.quantile(0.25)),
                "q3": float(income_data.quantile(0.75))
            },
            "records_with_income": len(income_data),
            "percentage_with_income_data": float(len(income_data) / len(df) * 100)
        }
    
    return analysis, df

def generate_sample_personas(df, n_samples=10):
    """Generate sample persona data based on real demographic patterns."""
    
    # Sample random records
    samples = df.sample(n=min(n_samples, len(df)))
    
    personas_data = []
    for _, row in samples.iterrows():
        persona = {
            "age": int(row['alter']) if pd.notna(row['alter']) else None,
            "gender": "Female" if row['weiblich'] == 1 else "Male",
            "family_status": row['fam_status'] if pd.notna(row['fam_status']) else "Unknown",
            "canton": row['kanton'] if pd.notna(row['kanton']) else "Unknown",
            "language_region": row['sprachgebiet'] if pd.notna(row['sprachgebiet']) else "Unknown",
            "education_level": row['bildungsniveau'] if pd.notna(row['bildungsniveau']) else "Unknown",
            "employment_status": row['erwerbsstatus'] if pd.notna(row['erwerbsstatus']) else "Unknown",
            "profession_category": row['beruf'] if pd.notna(row['beruf']) else "Unknown",
            "household_size": int(row['hhgroesse']) if pd.notna(row['hhgroesse']) else None,
            "has_children": bool(row['kinder']) if pd.notna(row['kinder']) else False,
            "annual_income_chf": int(row['bruttojahr']) if pd.notna(row['bruttojahr']) else None,
            "employment_percentage": int(row['beschaeftgrad']) if pd.notna(row['beschaeftgrad']) else None,
            "municipality_type": row['gemeindetyp'] if pd.notna(row['gemeindetyp']) else "Unknown",
            "region": row['grossregion'] if pd.notna(row['grossregion']) else "Unknown"
        }
        personas_data.append(persona)
    
    return personas_data

def create_enhanced_prompt_data(analysis, sample_personas):
    """Create enhanced prompt data based on demographic analysis."""
    
    prompt_enhancement = f"""
## Demographic Context for Swiss Banking Client Personas

Based on analysis of {analysis['total_records']:,} real Swiss demographic records, use the following patterns to create realistic personas:

### Age Distribution
- Average age: {analysis['age_distribution']['mean']:.1f} years
- Age range: {analysis['age_distribution']['min']}-{analysis['age_distribution']['max']} years
- Most common age groups: 25-40 (working age), 45-65 (established professionals)

### Gender Distribution
- Female: {analysis['gender_distribution']['female_percentage']:.1f}%
- Male: {analysis['gender_distribution']['male_percentage']:.1f}%

### Family Status Distribution
{chr(10).join([f"- {status}: {count:,} people" for status, count in list(analysis['family_status_distribution'].items())[:5]])}

### Regional Distribution (Top Cantons)
{chr(10).join([f"- {canton}: {count:,} people" for canton, count in list(analysis['canton_distribution'].items())[:8]])}

### Language Regions
{chr(10).join([f"- {region}: {count:,} people" for region, count in analysis['language_region_distribution'].items()])}

### Education Levels
{chr(10).join([f"- {level}: {count:,} people" for level, count in analysis['education_levels'].items()])}

### Employment Status
{chr(10).join([f"- {status}: {count:,} people" for status, count in analysis['employment_status'].items()])}

### Income Information
- Average annual income: CHF {analysis['income_distribution']['mean']:,.0f}
- Median annual income: CHF {analysis['income_distribution']['median']:,.0f}
- Income range (25th-75th percentile): CHF {analysis['income_distribution']['quartiles']['q1']:,.0f} - CHF {analysis['income_distribution']['quartiles']['q3']:,.0f}

### Example Real Demographic Patterns:
{chr(10).join([f"- {persona['age']}yr {persona['gender']}, {persona['family_status']}, {persona['canton']}, {persona['education_level']}, Income: CHF {persona['annual_income_chf']:,}" if persona['annual_income_chf'] else f"- {persona['age']}yr {persona['gender']}, {persona['family_status']}, {persona['canton']}, {persona['education_level']}" for persona in sample_personas[:5]])}

Use these realistic patterns to ensure your generated personas reflect actual Swiss demographic distributions.
"""
    
    return prompt_enhancement

def main():
    # Analyze the demographic data
    csv_path = "/Users/severin/Documents/GitHub/swiss-ai-weeks-finnova-banking-client-simulation/data/Demographie/datax.csv"
    
    print("Analyzing Swiss demographic data...")
    analysis, df = analyze_demographic_data(csv_path)
    
    # Generate sample personas
    sample_personas = generate_sample_personas(df, n_samples=20)
    
    # Create enhanced prompt data
    prompt_enhancement = create_enhanced_prompt_data(analysis, sample_personas)
    
    # Save analysis results
    with open('demographic_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    # Save sample personas
    with open('sample_demographic_personas.json', 'w', encoding='utf-8') as f:
        json.dump(sample_personas, f, indent=2, ensure_ascii=False)
    
    # Save prompt enhancement
    with open('demographic_prompt_enhancement.md', 'w', encoding='utf-8') as f:
        f.write(prompt_enhancement)
    
    print("\n✅ Analysis complete!")
    print("📊 Files created:")
    print("  - demographic_analysis.json (statistical analysis)")
    print("  - sample_demographic_personas.json (sample personas)")
    print("  - demographic_prompt_enhancement.md (prompt enhancement)")
    
    return analysis, sample_personas, prompt_enhancement

if __name__ == "__main__":
    main()