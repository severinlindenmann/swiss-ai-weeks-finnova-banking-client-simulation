import json
import time
import subprocess
import sys
import os
from pathlib import Path
import glob

def generate_large_persona_dataset(total_count=100, batch_size=20, output_file="personas_dataset_100.json"):
    """Generate a large dataset by creating multiple smaller batches."""
    
    print(f"🎭 Generating {total_count} personas in batches of {batch_size}")
    
    all_personas = []
    batches_needed = (total_count + batch_size - 1) // batch_size
    
    for batch_num in range(batches_needed):
        current_batch_size = min(batch_size, total_count - len(all_personas))
        
        print(f"\n📦 Batch {batch_num + 1}/{batches_needed}: Generating {current_batch_size} personas...")
        
        # Generate this batch
        batch_output = f"batch_{batch_num + 1}_{int(time.time())}"
        
        result = subprocess.run([
            sys.executable, "generate_personas.py",
            "--count", str(current_batch_size),
            "--output", batch_output
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error in batch {batch_num + 1}:")
            print(result.stderr)
            continue
        
        # Find the generated file
        pattern = f"{batch_output}-*.json"
        files = glob.glob(pattern)
        
        if not files:
            print(f"❌ No output file found for batch {batch_num + 1}")
            continue
        
        latest_file = max(files, key=os.path.getctime)
        
        # Load the batch data
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
            
            # Extract personas from the batch
            if isinstance(batch_data, dict) and 'personas' in batch_data:
                batch_personas = batch_data['personas']
            elif isinstance(batch_data, list):
                batch_personas = batch_data
            else:
                batch_personas = [batch_data]
            
            all_personas.extend(batch_personas)
            print(f"✅ Added {len(batch_personas)} personas (Total: {len(all_personas)})")
            
            # Clean up batch file
            Path(latest_file).unlink()
            
        except Exception as e:
            print(f"❌ Error processing batch {batch_num + 1}: {e}")
            continue
        
        # Small delay to avoid rate limits
        time.sleep(1)
    
    # Save the combined dataset
    final_dataset = {
        "metadata": {
            "total_personas": len(all_personas),
            "generated_at": int(time.time()),
            "batch_size": batch_size,
            "source": "enhanced_swiss_demographics"
        },
        "personas": all_personas
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Successfully generated {len(all_personas)} personas!")
    print(f"📁 Saved to: {output_file}")
    
    return output_file, len(all_personas)

if __name__ == "__main__":
    import os
    generate_large_persona_dataset(total_count=100, batch_size=15)