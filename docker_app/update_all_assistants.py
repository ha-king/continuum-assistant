#!/usr/bin/env python3
import os
import re

# List of all assistant files
assistant_files = [
    'math_assistant.py',
    'english_assistant.py', 
    'language_assistant.py',
    'computer_science_assistant.py',
    'financial_assistant.py',
    'aws_assistant.py',
    'business_dev_assistant.py',
    'lafayette_economic_assistant.py',
    'research_assistant.py',
    'louisiana_legal_assistant.py',
    'no_expertise.py',
    'psychology_assistant.py',
    'cryptography_assistant.py',
    'blockchain_assistant.py',
    'cryptocurrency_assistant.py',
    'tokenomics_assistant.py',
    'economics_assistant.py',
    'cybersecurity_offense_assistant.py',
    'cybersecurity_defense_assistant.py',
    'web3_assistant.py',
    'entrepreneurship_assistant.py',
    'ai_assistant.py',
    'microchip_supply_chain_assistant.py',
    'opensource_supply_chain_assistant.py',
    'nuclear_energy_assistant.py',
    'louisiana_vc_assistant.py',
    'data_acquisition_assistant.py',
    'data_analysis_assistant.py'
]

for file in assistant_files:
    if os.path.exists(file):
        with open(file, 'r') as f:
            content = f.read()
        
        # Add web browser import if not present
        if 'from web_browser_assistant import web_browser_assistant' not in content:
            content = content.replace(
                'from strands import Agent, tool',
                'from strands import Agent, tool\nfrom web_browser_assistant import web_browser_assistant'
            )
        
        # Add web browsing capability before agent creation
        agent_pattern = r'(\s+)(\w+_agent = Agent\(\s*system_prompt=\w+_SYSTEM_PROMPT,\s*tools=\[\],\s*\))'
        
        def add_web_capability(match):
            indent = match.group(1)
            agent_code = match.group(2)
            
            web_code = f'''{indent}# Add web browsing for current data if needed
{indent}if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):
{indent}    try:
{indent}        web_data = web_browser_assistant(f"Current research data: {{query}}")
{indent}        formatted_query += f"\\n\\nCurrent data from web: {{web_data}}"
{indent}    except:
{indent}        pass
{indent}
{indent}{agent_code}'''
            return web_code
        
        if re.search(agent_pattern, content):
            content = re.sub(agent_pattern, add_web_capability, content)
        
        with open(file, 'w') as f:
            f.write(content)
        
        print(f"Updated {file}")

print("All assistants updated with web browsing capability")