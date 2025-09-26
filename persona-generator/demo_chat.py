#!/usr/bin/env python3
"""
Demo script for the new Persona Chat functionality
"""

import json
import os
from persona_chat import load_all_personas, create_persona_chat_prompt

def demo_persona_chat():
    """Demonstrate the persona chat functionality"""
    
    print("🎭 Banking Persona Chat Demo")
    print("=" * 50)
    
    # Load personas
    print("📂 Loading generated personas...")
    personas = load_all_personas()
    
    if not personas:
        print("❌ No personas found!")
        print("💡 Generate some personas first using the Batch Generation page")
        return
    
    print(f"✅ Found {len(personas)} personas!")
    
    # Show available personas
    print("\n🎯 Available personas:")
    for i, persona in enumerate(personas[:5]):  # Show first 5
        persona_data = persona['data']['persona']
        basic_info = persona_data.get('basic_info', {})
        professional = persona_data.get('professional', {})
        
        name = basic_info.get('name', 'Unbekannt')
        age = basic_info.get('age', 'N/A')
        job = professional.get('job_title', 'N/A')
        print(f"  {i+1}. {name} ({age} Jahre, {job})")
    
    if len(personas) > 5:
        print(f"  ... and {len(personas) - 5} more personas")
    
    # Demo chat prompt creation
    print(f"\n💬 Demo chat prompt for first persona:")
    print("-" * 30)
    
    first_persona = personas[0]
    demo_conversation = "Benutzer: Hallo!\nPersona: Hallo! Schön dich kennenzulernen!"
    
    chat_prompt = create_persona_chat_prompt(first_persona['data'], demo_conversation)
    
    # Show key parts of the prompt
    lines = chat_prompt.split('\n')
    print("System prompt preview:")
    for line in lines[:10]:  # First 10 lines
        if line.strip():
            print(f"  {line}")
    print("  ... (truncated)")
    
    print(f"\n✨ Chat system is ready!")
    print("\n🚀 How to use:")
    print("1. Go to http://localhost:8501")
    print("2. Select 'Persona Chat' from the sidebar")  
    print("3. Enter your Swiss AI API key")
    print("4. Choose a persona from the dropdown")
    print("5. Start chatting!")
    
    print("\n💡 Example questions to try:")
    print("• 'Was hältst du von einem Sparplan mit 3% Zinsen?'")
    print("• 'Würdest du in Kryptowährungen investieren?'")
    print("• 'Wie gehst du mit deinen Finanzen um?'")
    print("• 'Brauchst du eine Hausratversicherung?'")

if __name__ == "__main__":
    demo_persona_chat()