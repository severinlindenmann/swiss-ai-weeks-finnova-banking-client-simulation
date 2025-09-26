import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("SWISS_AI_PLATFORM_API_KEY"),
    base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
)

response = client.chat.completions.create(
    model="swiss-ai/Apertus-70B",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that creates realistic banking client personas. Always respond with valid JSON format."},
        {"role": "user", "content": """Create exactly 20 diverse banking client personas for a banking client simulation. Each persona should include:
        - name (first and last name)
        - age
        - profession
        - annual_income (in CHF)
        - financial_goals (array of goals)
        - risk_tolerance (low, medium, high)
        - current_assets (in CHF)
        - monthly_expenses (in CHF)
        - family_status (single, married, divorced, etc.)
        - location (Swiss city)
        - banking_preferences (array of preferences like online banking, personal advisor, etc.)
        
        Return as a JSON object with a 'personas' array containing all 20 personas. Make sure each persona is unique and realistic for Swiss banking clients."""}
    ],
    stream=False
)

# Get the response content
content = response.choices[0].message.content
print("Generated response:")
print(content)

try:
    # Parse the JSON response
    personas_data = json.loads(content)
    
    # Save to JSON file
    with open('banking_personas.json', 'w', encoding='utf-8') as f:
        json.dump(personas_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully saved {len(personas_data.get('personas', []))} personas to 'banking_personas.json'")
    
except json.JSONDecodeError as e:
    print(f"\n❌ Error parsing JSON: {e}")
    print("Raw response saved to 'raw_response.txt' for debugging")
    with open('raw_response.txt', 'w', encoding='utf-8') as f:
        f.write(content)