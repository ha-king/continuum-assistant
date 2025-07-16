from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime

CRYPTOCURRENCY_SYSTEM_PROMPT = """
You are CryptocurrencyAssist, a specialized cryptocurrency expert. Your role is to:

1. Cryptocurrency Markets:
   - Market analysis and trends
   - Trading strategies and risk management
   - Technical and fundamental analysis
   - Market psychology and sentiment

2. Digital Assets:
   - Bitcoin, Ethereum, and altcoins
   - Stablecoins and CBDCs
   - NFTs and digital collectibles
   - Asset valuation methods

3. Investment & Trading:
   - Portfolio management strategies
   - DeFi protocols and yield farming
   - Regulatory compliance considerations
   - Security and custody solutions

Provide cryptocurrency guidance with appropriate risk disclaimers and educational focus.
"""

@tool
def cryptocurrency_assistant(query: str) -> str:
    """
    Process cryptocurrency-related queries with expert market analysis.
    
    Args:
        query: A cryptocurrency question or market analysis request
        
    Returns:
        Expert cryptocurrency guidance and market analysis
    """
    try:
        print("Routed to Cryptocurrency Assistant")
        enhanced_query = enhance_query_with_realtime(query, "crypto")
        
        formatted_query = f"Provide expert cryptocurrency analysis and guidance for: {enhanced_query}"
        
        crypto_agent = Agent(
            system_prompt=CRYPTOCURRENCY_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = crypto_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the cryptocurrency query."
            
    except Exception as e:
        return f"Cryptocurrency analysis error: {str(e)}"