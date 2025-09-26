#!/usr/bin/env python3
"""
Enhanced Banking Persona Generator
Generates realistic Swiss banking client personas using real demographic data.

Usage:
    python generate_personas.py --count 15 --output MY_CLIENTS
    python generate_personas.py --count 5 --focus-region zurich
    python generate_personas.py --count 20 --age-group working-age
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic Swiss banking client personas",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=20,
        help="Number of personas to generate (default: 20)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="BANKING_PERSONAS",
        help="Output file prefix (default: BANKING_PERSONAS)"
    )
    
    parser.add_argument(
        "--prompt-type",
        choices=["basic", "enhanced"],
        default="enhanced",
        help="Type of prompt to use (default: enhanced with demographic data)"
    )
    
    parser.add_argument(
        "--analyze-demographics",
        action="store_true",
        help="Re-analyze demographic data before generating personas"
    )
    
    args = parser.parse_args()
    
    # Change to the demo directory
    demo_dir = Path(__file__).parent
    os.chdir(demo_dir)
    
    # Re-analyze demographics if requested
    if args.analyze_demographics:
        print("🔍 Re-analyzing demographic data...")
        result = subprocess.run([
            sys.executable, "analyze_demographics.py"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Error analyzing demographics:")
            print(result.stderr)
            sys.exit(1)
        else:
            print("✅ Demographic analysis updated!")
    
    # Choose prompt file
    if args.prompt_type == "enhanced":
        prompt_file = "prompts/enhanced_demo.md"
    else:
        prompt_file = "prompts/demo.md"
    
    # Generate personas
    print(f"🎭 Generating {args.count} personas using {args.prompt_type} prompt...")
    
    result = subprocess.run([
        sys.executable, "prompt.py",
        prompt_file,
        "--examples", str(args.count),
        "--output", args.output
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Error generating personas:")
        print(result.stderr)
        sys.exit(1)
    else:
        print(result.stdout)
        
        # Find the generated file
        import re
        import glob
        
        # Look for the generated file
        pattern = f"{args.output}-*.json"
        files = glob.glob(pattern)
        
        if files:
            latest_file = max(files, key=os.path.getctime)
            print(f"\n🎉 Personas generated successfully!")
            print(f"📁 File: {latest_file}")
            
            # Show a quick preview
            import json
            try:
                with open(latest_file, 'r') as f:
                    data = json.load(f)
                    if 'personas' in data:
                        count = len(data['personas'])
                        print(f"👥 Generated {count} personas")
                        
                        # Show first persona as preview
                        if data['personas']:
                            first = data['personas'][0]
                            print(f"📋 Preview: {first.get('name', 'N/A')}, {first.get('age', 'N/A')}yr, {first.get('location', 'N/A')}, CHF {first.get('annual_income', 'N/A'):,}/yr")
            except Exception as e:
                print(f"⚠️  Could not preview file: {e}")

if __name__ == "__main__":
    main()