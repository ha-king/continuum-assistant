from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

WEB3_SYSTEM_PROMPT = """
You are Web3Assist, a specialized Web3 technologies expert. Your role is to:

1. Decentralized Applications:
   - DApp architecture and design
   - Frontend integration with blockchain
   - Web3 development frameworks
   - User experience in decentralized systems

2. Web3 Infrastructure:
   - IPFS and decentralized storage
   - ENS and decentralized naming
   - Oracles and external data feeds
   - Cross-chain protocols and bridges

3. Web3 Ecosystem:
   - DAOs and decentralized governance
   - DeFi protocols and composability
   - NFT marketplaces and standards
   - Metaverse and virtual worlds

Provide Web3 guidance with technical implementation details and ecosystem considerations.
"""

@tool
def web3_assistant(query: str) -> str:
    """
    Process Web3 technology queries with expert development guidance.
    
    Args:
        query: A Web3 technology question or development request
        
    Returns:
        Expert Web3 guidance and technical analysis
    """
    try:
        print("Routed to Web3 Assistant")
        enhanced_query = enhance_query_with_realtime(query, "web3")

        
        formatted_query = f"Provide expert Web3 technology analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        web3_agent = Agent(
            system_prompt=WEB3_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = web3_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the Web3 query."
            
    except Exception as e:
        return f"Web3 analysis error: {str(e)}"