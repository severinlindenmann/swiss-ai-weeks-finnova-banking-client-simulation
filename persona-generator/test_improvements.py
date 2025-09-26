#!/usr/bin/env python3
"""
Quick demo of the improved persona chat with .env integration
"""

import os
from dotenv import load_dotenv

def test_env_integration():
    """Test .env file integration"""
    
    print("🔧 Testing .env Integration")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("SWISS_AI_PLATFORM_API_KEY")
    
    if api_key:
        print("✅ API Key loaded from .env")
        print(f"🔑 Key preview: {api_key[:8]}...")
        print("✅ Ready for automatic authentication")
    else:
        print("❌ No API key found in .env")
        print("💡 Make sure .env contains: SWISS_AI_PLATFORM_API_KEY=your_key")
    
    print(f"\n🚀 Improvements:")
    print("• Auto-loads API key from .env file")  
    print("• Shorter, more concise responses (200 tokens vs 500)")
    print("• Streamlined UI with compact labels")
    print("• Faster interaction with reduced text")
    
    print(f"\n💬 Ready to chat!")
    print("Go to: http://localhost:8501 → Persona Chat")

if __name__ == "__main__":
    test_env_integration()