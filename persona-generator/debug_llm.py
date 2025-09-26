#!/usr/bin/env python3
"""
Debug script to test LLM persona generation directly
"""
import json
from pathlib import Path
from data import load_demographie_csv
from llm import SwissAIClient

def load_prompt_files():
    """Load system and prompt markdown files"""
    system_path = Path(__file__).parent / "system.md"
    prompt_path = Path(__file__).parent / "prompt.md"
    
    with open(system_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    return system_prompt, prompt_template

def test_persona_generation():
    """Test persona generation with debug output"""
    
    print("🔍 Loading data...")
    df = load_demographie_csv()
    
    # Select first person for consistent testing
    selected_person = df.iloc[0]
    
    # Create test parameters
    additional_params = {
        'vermoegen': '10k-100k',
        'verfuegbares_einkommen': '60k-100k', 
        'grosse_ausgaben': 'ja',
        'eigentum': 1,
        'finanz_erfahrung': 'Fortgeschritten'
    }
    
    # Format statistical data
    person_dict = selected_person.to_dict()
    statistical_data_lines = []
    for key, value in person_dict.items():
        if pd.notna(value):
            statistical_data_lines.append(f"{key}: {value}")
    statistical_data_str = "\n".join(statistical_data_lines)
    
    # Prepare template variables
    combined_dict = {**person_dict, **additional_params}
    alter = combined_dict.get('alter', 'N/A')
    geschlecht = 'w' if combined_dict.get('weiblich', 0) == 1 else 'm'
    beruf = combined_dict.get('beruf', 'N/A')
    kinder = combined_dict.get('kinder', 0)
    single = combined_dict.get('ledig', 0)
    
    print("📋 Selected person data:")
    print(f"  Age: {alter}, Gender: {geschlecht}, Job: {beruf}")
    print(f"  Children: {kinder}, Single: {single}")
    print()
    
    # Load prompts
    system_prompt, prompt_template = load_prompt_files()
    
    # Fill template
    full_prompt = prompt_template.format(
        statistical_data=statistical_data_str,
        alter=alter,
        geschlecht=geschlecht,
        vermoegen=additional_params['vermoegen'],
        verfuegbares_einkommen=additional_params['verfuegbares_einkommen'],
        grosse_ausgaben=additional_params['grosse_ausgaben'],
        beruf=beruf,
        kinder=kinder,
        eigentum=additional_params['eigentum'],
        single=single,
        finanz_erfahrung=additional_params['finanz_erfahrung']
    )
    
    print("🤖 System Prompt (first 500 chars):")
    print(system_prompt[:500] + "..." if len(system_prompt) > 500 else system_prompt)
    print()
    
    print("📝 User Prompt (first 1000 chars):")
    print(full_prompt[:1000] + "..." if len(full_prompt) > 1000 else full_prompt)
    print()
    
    print("🚀 Calling LLM...")
    try:
        client = SwissAIClient()
        
        response = client.complete(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=3000
        )
        
        print("✅ LLM Response received!")
        print("📄 Raw Response:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        print()
        
        # Try to parse JSON
        response_clean = response.strip()
        
        # Remove markdown
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]
        elif response_clean.startswith("```"):
            response_clean = response_clean[3:]
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]
        
        response_clean = response_clean.strip()
        
        # Find JSON boundaries
        json_start = response_clean.find('{')
        json_end = response_clean.rfind('}')
        
        if json_start != -1 and json_end != -1 and json_end > json_start:
            json_part = response_clean[json_start:json_end+1]
            
            print("🧹 Cleaned JSON:")
            print("-" * 80)
            print(json_part)
            print("-" * 80)
            print()
            
            try:
                parsed = json.loads(json_part)
                print("✅ JSON parsing successful!")
                print("🎯 Persona ID:", parsed.get('persona_id', 'N/A'))
                
                if 'basic_info' in parsed:
                    basic = parsed['basic_info']
                    print(f"👤 Name: {basic.get('name', 'N/A')}")
                    print(f"📍 Age: {basic.get('age', 'N/A')}")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"Error at position {e.pos}: {e.msg}")
                
                # Show problem area
                start = max(0, e.pos - 50)
                end = min(len(json_part), e.pos + 50)
                problem_area = json_part[start:end]
                print(f"Problem area: ...{problem_area}...")
                
                # Try to fix by removing comments
                print("\n🔧 Attempting to fix JSON by removing comments...")
                try:
                    import re
                    # Remove JavaScript-style comments
                    fixed_json = re.sub(r'//.*$', '', json_part, flags=re.MULTILINE)
                    # Remove trailing commas
                    fixed_json = re.sub(r',\s*}', '}', fixed_json)
                    fixed_json = re.sub(r',\s*]', ']', fixed_json)
                    # Clean up extra whitespace
                    fixed_json = re.sub(r'\n\s*\n', '\n', fixed_json)
                    
                    parsed = json.loads(fixed_json)
                    print("✅ JSON fix successful!")
                    print("🎯 Persona ID:", parsed.get('persona_id', 'N/A'))
                    return True
                except Exception as fix_e:
                    print(f"❌ JSON fix failed: {fix_e}")
                    return False
        else:
            print("❌ Could not find JSON boundaries in response")
            return False
            
    except Exception as e:
        print(f"❌ Error calling LLM: {e}")
        return False

if __name__ == "__main__":
    import pandas as pd
    test_persona_generation()