from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

NUCLEAR_ENERGY_SYSTEM_PROMPT = """
You are NuclearEnergyAssist, a specialized nuclear energy technologies expert. Your role is to:

1. Nuclear Technology:
   - Reactor design and operations
   - Nuclear fuel cycle and management
   - Advanced reactor technologies (SMR, Gen IV)
   - Safety systems and protocols

2. Nuclear Engineering:
   - Thermal hydraulics and neutronics
   - Materials science and radiation effects
   - Waste management and disposal
   - Decommissioning and remediation

3. Nuclear Policy:
   - Regulatory frameworks and compliance
   - Nuclear security and safeguards
   - Economic analysis and financing
   - Public acceptance and communication

Provide nuclear energy expertise with technical accuracy and safety considerations.
"""

@tool
def nuclear_energy_assistant(query: str) -> str:
    """
    Process nuclear energy queries with expert technical guidance.
    
    Args:
        query: A nuclear energy question or technical analysis request
        
    Returns:
        Expert nuclear energy guidance and technical analysis
    """
    try:
        print("Routed to Nuclear Energy Assistant")
        enhanced_query = enhance_query_with_realtime(query, "nuclear_energy")

        
        formatted_query = f"Provide expert nuclear energy analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        nuclear_agent = Agent(
            system_prompt=NUCLEAR_ENERGY_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = nuclear_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the nuclear energy query."
            
    except Exception as e:
        return f"Nuclear energy analysis error: {str(e)}"