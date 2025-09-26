import os
import json
import openai
import argparse
import time
import re
from pathlib import Path
from dotenv import load_dotenv

def parse_markdown_prompt(file_path, num_examples=20):
    """Parse a markdown file to extract system and user prompts."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by markdown headers
    lines = content.split('\n')
    system_prompt = ""
    user_prompt = ""
    current_section = None
    
    for line in lines:
        if line.strip().startswith('## System Prompt'):
            current_section = 'system'
        elif line.strip().startswith('## User Prompt'):
            current_section = 'user'
        elif line.strip().startswith('#') and not line.strip().startswith('##'):
            current_section = None
        elif current_section == 'system' and line.strip() and not line.strip().startswith('#'):
            system_prompt += line + '\n'
        elif current_section == 'user' and line.strip() and not line.strip().startswith('#'):
            user_prompt += line + '\n'
    
    # Replace number placeholders in the user prompt
    user_prompt = re.sub(r'\b(\d+)\b', str(num_examples), user_prompt.strip())
    
    return system_prompt.strip(), user_prompt

def run_prompt(prompt_file_path, num_examples=20):
    """Run a prompt from a markdown file and save the response."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Parse the markdown file
    system_prompt, user_prompt = parse_markdown_prompt(prompt_file_path, num_examples)
    
    if not system_prompt or not user_prompt:
        raise ValueError("Could not find both system and user prompts in the markdown file")
    
    print(f"System Prompt: {system_prompt[:100]}...")
    print(f"User Prompt: {user_prompt[:100]}...")
    
    # Initialize OpenAI client
    client = openai.OpenAI(
        api_key=os.getenv("SWISS_AI_PLATFORM_API_KEY"),
        base_url="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
    )
    
    # Create the chat completion
    response = client.chat.completions.create(
        model="swiss-ai/Apertus-70B",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=False
    )
    
    return response

def main():
    """Main function to handle command line arguments and execution."""
    parser = argparse.ArgumentParser(description="Run OpenAI prompts from markdown files")
    parser.add_argument("prompt_file", 
                       help="Path to the markdown prompt file (e.g., demo.md)")
    parser.add_argument("--examples", "-n", 
                       type=int, default=20,
                       help="Number of examples to generate (default: 20)")
    parser.add_argument("--output", "-o", 
                       help="Output file prefix (default: OUTPUT)")
    
    args = parser.parse_args()
    
    # Resolve the prompt file path
    prompt_path = Path(args.prompt_file)
    if not prompt_path.is_absolute():
        prompt_path = Path(__file__).parent / prompt_path
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    # Generate output filename with timestamp
    timestamp = int(time.time())
    output_prefix = args.output or "OUTPUT"
    output_name = f"{output_prefix}-{timestamp}.json"
    
    print(f"Running prompt from: {prompt_path}")
    print(f"Generating {args.examples} examples")
    print(f"Output will be saved to: {output_name}")
    
    # Run the prompt
    response = run_prompt(prompt_path, args.examples)

    # Get the response content
    content = response.choices[0].message.content
    print("\nGenerated response:")
    print(content[:500] + "..." if len(content) > 500 else content)

    try:
        # Clean the content by removing markdown code blocks and fixing common issues
        cleaned_content = content.strip()
        
        # Remove markdown code blocks if present
        if cleaned_content.startswith('```json'):
            cleaned_content = cleaned_content[7:]  # Remove ```json
        elif cleaned_content.startswith('```'):
            cleaned_content = cleaned_content[3:]   # Remove ```
            
        if cleaned_content.endswith('```'):
            cleaned_content = cleaned_content[:-3]  # Remove trailing ```
        
        # Find JSON content between curly braces if truncated
        start_idx = cleaned_content.find('{')
        if start_idx != -1:
            # Find the last complete closing brace
            brace_count = 0
            last_valid_end = -1
            for i, char in enumerate(cleaned_content[start_idx:], start_idx):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        last_valid_end = i + 1
                        break
            
            if last_valid_end != -1:
                cleaned_content = cleaned_content[start_idx:last_valid_end]
            else:
                cleaned_content = cleaned_content[start_idx:]
        
        cleaned_content = cleaned_content.strip()
        
        # Parse the JSON response
        response_data = json.loads(cleaned_content)
        
        # Save to JSON file
        with open(output_name, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
        
        # Count items if it's an array structure
        if isinstance(response_data, dict) and 'personas' in response_data:
            count = len(response_data.get('personas', []))
            print(f"\n✅ Successfully saved {count} personas to '{output_name}'")
        elif isinstance(response_data, dict):
            # Count top-level keys or items in arrays
            total_items = sum(len(v) if isinstance(v, list) else 1 for v in response_data.values())
            print(f"\n✅ Successfully saved {total_items} items to '{output_name}'")
        else:
            print(f"\n✅ Successfully saved response to '{output_name}'")
        
    except json.JSONDecodeError as e:
        print(f"\n❌ Error parsing JSON: {e}")
        timestamp = int(time.time())
        raw_filename = f"{output_prefix}-{timestamp}_raw_response.txt"
        print(f"Raw response saved to '{raw_filename}' for debugging")
        with open(raw_filename, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    main()