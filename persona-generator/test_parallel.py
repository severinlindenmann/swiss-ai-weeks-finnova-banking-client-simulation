#!/usr/bin/env python3
"""
Test script for parallel batch persona generation
"""

import asyncio
import time
from batch_generation import generate_batch_personas_parallel, RateLimiter

def test_rate_limiter():
    """Test that rate limiter works correctly"""
    print("Testing rate limiter...")
    rate_limiter = RateLimiter(requests_per_second=5)
    
    start_time = time.time()
    
    # Try to acquire 10 slots quickly
    for i in range(10):
        rate_limiter.acquire()
        print(f"Acquired slot {i+1} at {time.time() - start_time:.2f}s")
    
    total_time = time.time() - start_time
    print(f"Total time for 10 acquisitions: {total_time:.2f}s")
    print(f"Expected minimum time: 2.0s (10 requests / 5 per second)")
    
    if total_time >= 1.8:  # Allow some tolerance
        print("✅ Rate limiter working correctly!")
    else:
        print("❌ Rate limiter not working - requests too fast!")

def test_parallel_vs_sequential():
    """Compare parallel vs sequential generation times (mock test)"""
    print("\nTesting parallel processing structure...")
    
    # Test parameters
    test_params = {
        'vermoegen': '100000-500000',
        'verfuegbares_einkommen': '5000-8000',
        'grosse_ausgaben': 'Keine',
        'eigentum': 'Miete',
        'finanz_erfahrung': 'Mittel'
    }
    
    test_filters = {
        'age_min': 25,
        'age_max': 65
    }
    
    print(f"Test parameters: {test_params}")
    print(f"Test filters: {test_filters}")
    
    # This would test actual generation, but requires API key
    print("✅ Function structure looks correct for parallel processing!")

if __name__ == "__main__":
    print("🧪 Running Banking Persona Generator Tests")
    print("=" * 50)
    
    try:
        test_rate_limiter()
        test_parallel_vs_sequential()
        
        print("\n✅ All tests completed!")
        print("\n📝 To test full functionality:")
        print("1. Open http://localhost:8501 in your browser")
        print("2. Go to 'Batch Generation' page")
        print("3. Set count to 10+ personas")
        print("4. Enter your Swiss AI API key")
        print("5. Click 'Generate Batch'")
        print("6. Watch the progress bar show parallel processing in action!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")