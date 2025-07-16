from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

BLOCKCHAIN_SYSTEM_PROMPT = """
You are BlockchainAssist, a specialized blockchain technology expert. Your role is to:

1. Blockchain Fundamentals:
   - Distributed ledger technology
   - Consensus mechanisms (PoW, PoS, DPoS)
   - Block structure and validation
   - Network architecture and nodes

2. Smart Contracts:
   - Smart contract development
   - Solidity and other languages
   - Contract security and auditing
   - Gas optimization techniques

3. Blockchain Platforms:
   - Ethereum, Bitcoin, and altcoins
   - Layer 2 solutions and scaling
   - Interoperability protocols
   - Enterprise blockchain solutions

Provide technical blockchain guidance with implementation best practices and security considerations.
"""

@tool
def blockchain_assistant(query: str) -> str:
    """
    Process blockchain technology queries with expert technical guidance.
    
    Args:
        query: A blockchain technology question or development request
        
    Returns:
        Expert blockchain guidance and technical analysis
    """
    try:
        print("Routed to Blockchain Assistant")
        enhanced_query = enhance_query_with_realtime(query, "blockchain")

        
        formatted_query = f"Provide expert blockchain technology analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        blockchain_agent = Agent(
            system_prompt=BLOCKCHAIN_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = blockchain_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the blockchain query."
            
    except Exception as e:
        return f"Blockchain analysis error: {str(e)}"