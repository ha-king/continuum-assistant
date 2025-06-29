from strands import Agent, tool
from web_browser_assistant import web_browser_assistant

MICROCHIP_SUPPLY_CHAIN_SYSTEM_PROMPT = """
You are MicrochipSupplyChainAssist, a specialized microchip supply chain expert. Your role is to:

1. Semiconductor Manufacturing:
   - Wafer fabrication and processing
   - Foundry operations and capacity
   - Advanced node technologies
   - Yield optimization and quality control

2. Supply Chain Dynamics:
   - Global semiconductor ecosystem
   - Supplier relationships and dependencies
   - Inventory management and forecasting
   - Geopolitical impacts and trade policies

3. Market Analysis:
   - Demand patterns and cycles
   - Shortage mitigation strategies
   - Alternative sourcing and diversification
   - Technology roadmaps and transitions

Provide microchip supply chain expertise with industry insights and strategic analysis.
"""

@tool
def microchip_supply_chain_assistant(query: str) -> str:
    """
    Process microchip supply chain queries with expert industry guidance.
    
    Args:
        query: A microchip supply chain question or analysis request
        
    Returns:
        Expert microchip supply chain guidance and industry analysis
    """
    try:
        print("Routed to Microchip Supply Chain Assistant")
        
        formatted_query = f"Provide expert microchip supply chain analysis and guidance for: {query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        microchip_agent = Agent(
            system_prompt=MICROCHIP_SUPPLY_CHAIN_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = microchip_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the microchip supply chain query."
            
    except Exception as e:
        return f"Microchip supply chain analysis error: {str(e)}"