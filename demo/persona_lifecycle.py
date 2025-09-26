import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import json

class PersonaLifecycleModel:
    """Model persona financial lifecycle from birth to death with Swiss context."""
    
    def __init__(self):
        self.life_stages = {
            "childhood": (0, 17),
            "education": (18, 24),
            "early_career": (25, 34),
            "career_growth": (35, 49),
            "peak_career": (50, 64),
            "retirement": (65, 85)
        }
        
        self.swiss_life_expectancy = 83.8  # Average Swiss life expectancy
        
    def calculate_lifecycle_trajectory(self, persona: Dict) -> Dict:
        """Calculate complete lifecycle financial trajectory for a persona."""
        
        current_age = persona['age']
        current_income = persona['annual_income']
        education_level = persona.get('education_level', 'Secondary Level II')
        location = persona.get('location', 'Zürich')
        
        # Base trajectory calculation
        trajectory = self._generate_base_trajectory(current_age, current_income, education_level, persona)
        
        # Add Swiss-specific factors
        trajectory = self._add_swiss_factors(trajectory, location, education_level)
        
        # Add life events
        trajectory = self._add_life_events(trajectory, persona)
        
        # Calculate financial milestones
        milestones = self._calculate_milestones(trajectory, persona)
        
        return {
            "current_age": current_age,
            "projected_life_expectancy": self.swiss_life_expectancy,
            "annual_trajectory": trajectory,
            "life_milestones": milestones,
            "retirement_projections": self._calculate_retirement_projections(trajectory, current_age)
        }
    
    def _generate_base_trajectory(self, current_age: int, current_income: int, education_level: str, persona: Dict = None) -> List[Dict]:
        """Generate base income and asset trajectory."""
        trajectory = []
        if persona is None:
            persona = {}
        
        # Education level income multipliers
        education_multipliers = {
            "Sekundarstufe I": 0.85,
            "Sekundarstufe II": 1.0,
            "Tertiaerstufe": 1.35
        }
        
        base_multiplier = education_multipliers.get(education_level, 1.0)
        
        for age in range(0, int(self.swiss_life_expectancy) + 1):
            if age < 18:
                # Childhood - no income, dependent
                income = 0
                assets = 0
                expenses = 0
            elif age < 25:
                # Education phase
                income = 15000 if age >= 18 else 0  # Part-time work
                expenses = 20000
                assets = max(0, income - expenses) if age == 18 else 0
            elif age < 35:
                # Early career - starting salary growing to current level
                career_progress = (age - 25) / 10
                if age <= current_age:
                    income = int(current_income * (0.6 + 0.4 * career_progress))
                else:
                    income = int(current_income * base_multiplier * (0.6 + 0.4 * career_progress))
                expenses = int(income * 0.7)
                assets = max(0, income - expenses)
            elif age < 50:
                # Career growth - peak earning potential
                career_peak = min(1.0, (age - 35) / 15 * 0.3 + 1.0)
                if age <= current_age:
                    income = current_income
                else:
                    income = int(current_income * base_multiplier * career_peak)
                expenses = int(income * 0.65)  # Better expense management
                assets = income - expenses
            elif age < 65:
                # Peak career - maintaining high income
                if age <= current_age:
                    income = current_income
                else:
                    income = int(current_income * base_multiplier * 1.2)
                expenses = int(income * 0.6)
                assets = income - expenses
            else:
                # Retirement - pension income
                pension_rate = 0.6  # Swiss pension system typically 60% replacement
                income = int(current_income * base_multiplier * pension_rate)
                expenses = int(income * 0.8)  # Lower expenses in retirement
                assets = income - expenses
            
            # Apply age to current situation
            if age == current_age:
                income = current_income
                assets = persona.get('current_assets', assets)
                expenses = persona.get('monthly_expenses', expenses // 12) * 12
            
            trajectory.append({
                "age": age,
                "annual_income": income,
                "annual_expenses": expenses,
                "annual_savings": max(0, income - expenses),
                "life_stage": self._get_life_stage(age),
                "cumulative_assets": 0  # Will be calculated later
            })
        
        # Calculate cumulative assets
        cumulative_assets = persona.get('current_assets', 0) if current_age < len(trajectory) else 0
        for i, year in enumerate(trajectory):
            if year["age"] <= current_age:
                if year["age"] == current_age:
                    cumulative_assets = persona.get('current_assets', 0)
                year["cumulative_assets"] = cumulative_assets
            else:
                # Project future assets with 3% annual growth (investment returns)
                cumulative_assets = cumulative_assets * 1.03 + year["annual_savings"]
                year["cumulative_assets"] = int(cumulative_assets)
        
        return trajectory
    
    def _add_swiss_factors(self, trajectory: List[Dict], location: str, education_level: str) -> List[Dict]:
        """Add Swiss-specific factors like regional cost differences, tax implications."""
        
        # Regional cost of living adjustments
        regional_multipliers = {
            "Zürich": 1.2,
            "Genf": 1.15,
            "Basel": 1.1,
            "Bern": 1.05,
            "Lausanne": 1.08,
            "Luzern": 1.0,
            "St. Gallen": 0.95,
            "Winterthur": 0.95
        }
        
        location_multiplier = regional_multipliers.get(location, 1.0)
        
        for year in trajectory:
            # Adjust expenses for regional cost of living
            year["annual_expenses"] = int(year["annual_expenses"] * location_multiplier)
            year["annual_savings"] = year["annual_income"] - year["annual_expenses"]
            
            # Swiss-specific considerations
            if year["age"] >= 25:
                # Add pension contributions (3-pillar system)
                year["pension_contributions"] = int(year["annual_income"] * 0.17)  # ~17% total
                year["annual_savings"] -= year["pension_contributions"]
        
        return trajectory
    
    def _add_life_events(self, trajectory: List[Dict], persona: Dict) -> List[Dict]:
        """Add major life events that impact finances."""
        
        family_status = persona.get('family_status', 'Single')
        has_children = persona.get('has_children', False)
        
        for year in trajectory:
            age = year["age"]
            
            # Marriage impact (typically age 28-35)
            if family_status in ["Verheiratet", "married"] and 28 <= age <= 35:
                year["life_event"] = "Marriage"
                year["annual_expenses"] += 15000  # Wedding and setup costs
            
            # Children impact (typically age 25-45)
            if has_children and 25 <= age <= 45:
                if 30 <= age <= 32:  # First child
                    year["life_event"] = "First Child"
                    year["annual_expenses"] += 20000
                elif 33 <= age <= 35:  # Second child
                    year["life_event"] = "Second Child"
                    year["annual_expenses"] += 15000
                elif age > 35:
                    year["annual_expenses"] += 25000  # Ongoing child costs
            
            # Home purchase (typically age 30-40)
            if 30 <= age <= 40 and year["cumulative_assets"] > 200000:
                year["life_event"] = "Home Purchase"
                year["annual_expenses"] += 30000  # Mortgage payments
            
            # Career changes
            if age in [35, 45]:
                year["life_event"] = f"Career Advancement at {age}"
                year["annual_income"] = int(year["annual_income"] * 1.15)
        
        return trajectory
    
    def _calculate_milestones(self, trajectory: List[Dict], persona: Dict) -> List[Dict]:
        """Calculate major financial milestones."""
        milestones = []
        
        for year in trajectory:
            age = year["age"]
            assets = year["cumulative_assets"]
            income = year["annual_income"]
            
            # Financial independence milestones
            if assets >= income * 1:  # 1 year expenses saved
                milestones.append({
                    "age": age,
                    "milestone": "Emergency Fund Complete",
                    "value": assets,
                    "description": f"Saved 1 year of expenses (CHF {assets:,})"
                })
            
            if assets >= 100000 and not any(m["milestone"] == "First 100k" for m in milestones):
                milestones.append({
                    "age": age,
                    "milestone": "First 100k",
                    "value": assets,
                    "description": f"First CHF 100,000 in assets"
                })
            
            if assets >= 500000 and not any(m["milestone"] == "Half Million" for m in milestones):
                milestones.append({
                    "age": age,
                    "milestone": "Half Million",
                    "value": assets,
                    "description": f"CHF 500,000 in assets"
                })
            
            if assets >= 1000000 and not any(m["milestone"] == "Millionaire" for m in milestones):
                milestones.append({
                    "age": age,
                    "milestone": "Millionaire",
                    "value": assets,
                    "description": f"First million CHF in assets"
                })
        
        return milestones
    
    def _calculate_retirement_projections(self, trajectory: List[Dict], current_age: int) -> Dict:
        """Calculate retirement readiness and projections."""
        
        retirement_years = [year for year in trajectory if year["age"] >= 65]
        working_years = [year for year in trajectory if 25 <= year["age"] < 65]
        
        if not retirement_years or not working_years:
            return {}
        
        retirement_assets = retirement_years[0]["cumulative_assets"] if retirement_years else 0
        avg_working_income = np.mean([year["annual_income"] for year in working_years])
        
        return {
            "retirement_age": 65,
            "projected_retirement_assets": retirement_assets,
            "income_replacement_ratio": retirement_assets * 0.04 / avg_working_income if avg_working_income > 0 else 0,  # 4% rule
            "years_to_retirement": max(0, 65 - current_age),
            "monthly_retirement_income": int(retirement_assets * 0.04 / 12) if retirement_assets > 0 else 0
        }
    
    def _get_life_stage(self, age: int) -> str:
        """Get life stage for given age."""
        for stage, (start, end) in self.life_stages.items():
            if start <= age <= end:
                return stage
        return "elderly"

def enhance_personas_with_lifecycle(personas_file: str) -> str:
    """Enhance existing personas with lifecycle projections."""
    
    lifecycle_model = PersonaLifecycleModel()
    
    # Load personas
    with open(personas_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    personas = data.get('personas', [])
    
    # Add lifecycle data to each persona
    enhanced_personas = []
    for persona in personas:
        try:
            lifecycle_data = lifecycle_model.calculate_lifecycle_trajectory(persona)
            enhanced_persona = {**persona, "lifecycle": lifecycle_data}
            enhanced_personas.append(enhanced_persona)
        except Exception as e:
            print(f"Error processing persona {persona.get('name', 'Unknown')}: {e}")
            enhanced_personas.append(persona)  # Add without lifecycle data
    
    # Save enhanced dataset
    enhanced_data = {
        **data,
        "personas": enhanced_personas,
        "lifecycle_enhanced": True
    }
    
    enhanced_file = personas_file.replace('.json', '_with_lifecycle.json')
    with open(enhanced_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Enhanced {len(enhanced_personas)} personas with lifecycle data")
    print(f"📁 Saved to: {enhanced_file}")
    
    return enhanced_file

if __name__ == "__main__":
    # Test with existing personas
    import glob
    import os
    
    # Find most recent personas file
    persona_files = glob.glob("*PERSONAS*.json")
    if persona_files:
        latest_file = max(persona_files, key=lambda f: os.path.getctime(f))
        print(f"Enhancing {latest_file} with lifecycle data...")
        enhance_personas_with_lifecycle(latest_file)
    else:
        print("No persona files found to enhance.")