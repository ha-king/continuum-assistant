from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

TOKENOMICS_SYSTEM_PROMPT = """
You are TokenomicsAssist, a specialized tokenomics expert. Your role is to:

1. Token Design:
   - Token utility and value accrual
   - Supply mechanisms and inflation models
   - Distribution strategies and vesting
   - Governance token structures

2. Economic Models:
   - Token velocity and circulation
   - Incentive alignment mechanisms
   - Staking and reward systems
   - Burn mechanisms and deflationary models

3. Protocol Economics:
   - Fee structures and revenue models
   - Liquidity mining and yield farming
   - Treasury management strategies
   - Sustainable tokenomics design

Provide tokenomics guidance with economic modeling and sustainability considerations.
"""

@tool
def tokenomics_assistant(query: str) -> str:
    """
    Process tokenomics-related queries with expert economic analysis.
    
    Args:
        query: A tokenomics question or economic model request
        
    Returns:
        Expert tokenomics guidance and economic analysis
    """
    try:
        print("Routed to Tokenomics Assistant")
        enhanced_query = enhance_query_with_realtime(query, "tokenomics")

        
        formatted_query = f"Provide expert tokenomics analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        tokenomics_agent = Agent(
            system_prompt=TOKENOMICS_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = tokenomics_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the tokenomics query."
            
    except Exception as e:
        return f"Tokenomics analysis error: {str(e)}"