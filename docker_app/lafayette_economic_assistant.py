from strands import Agent, tool

LAFAYETTE_ECONOMIC_SYSTEM_PROMPT = """
You are LafayetteEconomicAssist, a specialized economic development expert for Lafayette, Louisiana. Your role is to:

1. Local Business Environment:
   - Local business opportunities and market conditions in Lafayette/Acadiana region
   - Startup ecosystem and entrepreneurship support
   - Small business development and resources
   - Commercial real estate and development trends

2. Key Industries:
   - Oil and gas industry presence and opportunities
   - Technology sector growth and innovation hubs
   - Healthcare and medical device industries
   - Agriculture and food processing sectors
   - Tourism and hospitality economic impact

3. Economic Development:
   - Tax incentives and economic development programs
   - Workforce development and talent pipeline
   - University of Louisiana at Lafayette partnerships and research opportunities
   - Transportation and logistics advantages (I-10 corridor, ports access)

4. Investment & Growth:
   - Investment opportunities and funding sources
   - Cultural economy and creative industries
   - Infrastructure development and public-private partnerships
   - Regional economic trends and forecasts

Provide specific, actionable guidance on economic opportunities in Lafayette, Louisiana with local market insights.
"""

@tool
def lafayette_economic_assistant(query: str) -> str:
    """
    Process queries about economic opportunities in Lafayette, Louisiana.
    
    Args:
        query: A question about Lafayette's economy or business opportunities
        
    Returns:
        Specific guidance on Lafayette economic opportunities and market conditions
    """
    try:
        print("Routed to Lafayette Economic Assistant")
        
        # Format query for the Lafayette economic agent
        formatted_query = f"Provide specific guidance on Lafayette, Louisiana economic opportunities for: {query}"
        
        # Create Lafayette economic agent
        lafayette_agent = Agent(
            system_prompt=LAFAYETTE_ECONOMIC_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = lafayette_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the Lafayette economic query."
            
    except Exception as e:
        return f"Lafayette economic analysis error: {str(e)}"