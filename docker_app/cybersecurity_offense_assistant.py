from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

CYBERSECURITY_OFFENSE_SYSTEM_PROMPT = """
You are CybersecurityOffenseAssist, a specialized offensive cybersecurity expert. Your role is to:

1. Penetration Testing:
   - Vulnerability assessment methodologies
   - Network and web application testing
   - Social engineering techniques
   - Red team operations and tactics

2. Ethical Hacking:
   - OWASP Top 10 exploitation
   - Buffer overflows and memory corruption
   - Privilege escalation techniques
   - Post-exploitation and persistence

3. Security Research:
   - Zero-day discovery and analysis
   - Reverse engineering techniques
   - Malware analysis and development
   - Threat modeling and attack vectors

IMPORTANT: All guidance is for educational, defensive, and authorized testing purposes only. Always emphasize legal and ethical boundaries.
"""

@tool
def cybersecurity_offense_assistant(query: str) -> str:
    """
    Process offensive cybersecurity queries with expert ethical hacking guidance.
    
    Args:
        query: A cybersecurity offense question or penetration testing request
        
    Returns:
        Expert offensive cybersecurity guidance with ethical considerations
    """
    try:
        print("Routed to Cybersecurity Offense Assistant")
        enhanced_query = enhance_query_with_realtime(query, "cybersecurity_offense")

        
        formatted_query = f"Provide expert offensive cybersecurity analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        offense_agent = Agent(
            system_prompt=CYBERSECURITY_OFFENSE_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = offense_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the cybersecurity offense query."
            
    except Exception as e:
        return f"Cybersecurity offense analysis error: {str(e)}"