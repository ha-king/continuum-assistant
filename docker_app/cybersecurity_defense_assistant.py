from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

CYBERSECURITY_DEFENSE_SYSTEM_PROMPT = """
You are CybersecurityDefenseAssist, a specialized defensive cybersecurity expert. Your role is to:

1. Security Architecture:
   - Defense-in-depth strategies
   - Network security design
   - Identity and access management
   - Security controls implementation

2. Incident Response:
   - Threat detection and analysis
   - Incident handling procedures
   - Digital forensics techniques
   - Recovery and remediation

3. Security Operations:
   - SIEM and security monitoring
   - Vulnerability management
   - Security awareness training
   - Compliance and governance

Provide defensive cybersecurity guidance with practical implementation strategies and best practices.
"""

@tool
def cybersecurity_defense_assistant(query: str) -> str:
    """
    Process defensive cybersecurity queries with expert security guidance.
    
    Args:
        query: A cybersecurity defense question or security implementation request
        
    Returns:
        Expert defensive cybersecurity guidance and best practices
    """
    try:
        print("Routed to Cybersecurity Defense Assistant")
        enhanced_query = enhance_query_with_realtime(query, "cybersecurity_defense")

        
        formatted_query = f"Provide expert defensive cybersecurity analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        defense_agent = Agent(
            system_prompt=CYBERSECURITY_DEFENSE_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = defense_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the cybersecurity defense query."
            
    except Exception as e:
        return f"Cybersecurity defense analysis error: {str(e)}"