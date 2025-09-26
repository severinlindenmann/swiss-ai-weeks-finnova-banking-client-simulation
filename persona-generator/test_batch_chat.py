#!/usr/bin/env python3
"""
Test script for the new Batch Chat functionality
"""

from batch_chat import load_persona_batches

def test_batch_chat():
    """Test batch chat functionality"""
    
    print("👥 Batch Chat Demo")
    print("=" * 40)
    
    # Load batches
    print("📦 Loading persona batches...")
    batches = load_persona_batches()
    
    if not batches:
        print("❌ No batches found!")
        print("💡 Generate some persona batches first")
        return
    
    print(f"✅ Found {len(batches)} batches!")
    
    # Show available batches
    print("\n🎯 Available batches:")
    for i, batch in enumerate(batches):
        print(f"  {i+1}. {batch['display_name']}")
        print(f"     └─ {batch['count']} personas")
    
    # Show first batch details
    if batches:
        first_batch = batches[0]
        print(f"\n📋 First batch details:")
        print(f"  Name: {first_batch['display_name']}")
        print(f"  Personas: {first_batch['count']}")
        
        # Show first few personas
        personas = first_batch['personas'][:3]
        print(f"  Sample personas:")
        for persona in personas:
            basic_info = persona['persona'].get('basic_info', {})
            name = basic_info.get('name', 'Unknown')
            age = basic_info.get('age', 'N/A')
            job = persona['persona'].get('professional', {}).get('job_title', 'N/A')
            print(f"    • {name} ({age}, {job})")
    
    print(f"\n🚀 Batch Chat Features:")
    print("• Select persona batch from dropdown")
    print("• Ask questions to multiple personas simultaneously")
    print("• Get diverse opinions on product ideas")
    print("• Parallel API calls for faster responses")
    print("• Built-in product idea buttons")
    
    print(f"\n💡 Example use cases:")
    print("• 'Was haltet ihr von einer Banking-App mit KI-Assistent?'")
    print("• 'Braucht ihr eine Kreditkarte mit nachhaltigen Rewards?'")
    print("• 'Wie wichtig ist euch digitale Hypotheken-Beratung?'")
    
    print(f"\n💬 Ready to test!")
    print("Go to: http://localhost:8501 → Batch Chat")

if __name__ == "__main__":
    test_batch_chat()