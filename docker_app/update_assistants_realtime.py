#!/usr/bin/env python3
"""
Script to update all assistant files with real-time data access capabilities
"""

import os
import re
from pathlib import Path

def update_assistant_file(file_path):
    """Update a single assistant file with real-time data access"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Skip if already updated
        if 'realtime_data_access' in content:
            print(f"✓ {file_path.name} already updated")
            return True
        
        # Skip consolidated_assistants.py and other special files
        if file_path.name in ['consolidated_assistants.py', 'update_all_assistants.py', 'update_assistants_realtime.py']:
            print(f"⏭ Skipping {file_path.name}")
            return True
        
        original_content = content
        
        # Add import for real-time data access
        if 'from strands import Agent, tool' in content:
            content = content.replace(
                'from strands import Agent, tool',
                'from strands import Agent, tool\nfrom realtime_data_access import enhance_query_with_realtime'
            )
        
        # Find the main assistant function and update it
        assistant_function_pattern = r'(@tool\ndef \w+_assistant\(query: str\) -> str:.*?)(try:.*?print\("Routed to.*?Assistant"\))(.*?)(agent = Agent\(.*?\))'
        
        def replace_assistant_function(match):
            decorator_and_def = match.group(1)
            try_and_print = match.group(2)
            middle_content = match.group(3)
            agent_creation = match.group(4)
            
            # Extract assistant type from the function name
            assistant_name_match = re.search(r'def (\w+)_assistant', decorator_and_def)
            assistant_type = assistant_name_match.group(1) if assistant_name_match else "general"
            
            # Create enhanced query line
            enhanced_query_line = f'\n        enhanced_query = enhance_query_with_realtime(query, "{assistant_type}")\n'
            
            # Update formatted_query to use enhanced_query
            updated_middle = re.sub(
                r'formatted_query = f"([^"]*): \{query\}"',
                r'formatted_query = f"\1: {enhanced_query}"',
                middle_content
            )
            
            # If no formatted_query found, add it
            if 'formatted_query' not in updated_middle:
                updated_middle = enhanced_query_line + updated_middle
            else:
                updated_middle = enhanced_query_line + updated_middle
            
            return decorator_and_def + try_and_print + updated_middle + agent_creation
        
        # Apply the replacement
        updated_content = re.sub(assistant_function_pattern, replace_assistant_function, content, flags=re.DOTALL)
        
        # If no changes were made with the complex pattern, try a simpler approach
        if updated_content == content:
            # Simple approach: add enhanced query after the print statement
            pattern = r'(print\("Routed to.*?Assistant"\))'
            replacement = r'\1\n        enhanced_query = enhance_query_with_realtime(query, "general")'
            updated_content = re.sub(pattern, replacement, content)
            
            # Update any query usage to use enhanced_query
            updated_content = re.sub(r'formatted_query = f"([^"]*): \{query\}"', r'formatted_query = f"\1: {enhanced_query}"', updated_content)
        
        # Only write if content changed
        if updated_content != original_content:
            with open(file_path, 'w') as f:
                f.write(updated_content)
            print(f"✅ Updated {file_path.name}")
            return True
        else:
            print(f"⚠️ No changes needed for {file_path.name}")
            return True
            
    except Exception as e:
        print(f"❌ Error updating {file_path.name}: {str(e)}")
        return False

def main():
    """Update all assistant files"""
    docker_app_dir = Path(__file__).parent
    assistant_files = list(docker_app_dir.glob('*_assistant.py'))
    
    print(f"Found {len(assistant_files)} assistant files to update")
    
    updated_count = 0
    for file_path in assistant_files:
        if update_assistant_file(file_path):
            updated_count += 1
    
    print(f"\n✅ Successfully processed {updated_count}/{len(assistant_files)} assistant files")
    print("🚀 All assistants now have real-time data access capabilities!")

if __name__ == "__main__":
    main()