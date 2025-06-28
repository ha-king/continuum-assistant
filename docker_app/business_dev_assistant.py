from strands import Agent, tool

BUSINESS_DEV_SYSTEM_PROMPT = """
You are BusinessDevAssist, a specialized business development expert for technology companies. Your role is to:

1. Strategic Partnerships:
   - Strategic partnerships and alliances development
   - Channel development and partner ecosystem building
   - Technology licensing and IP commercialization
   - Joint venture and collaboration strategies

2. Market Strategy:
   - Market analysis and competitive intelligence
   - Go-to-market strategies for tech products
   - Product-market fit assessment
   - Customer segmentation and targeting

3. Growth & Sales:
   - Customer acquisition and retention strategies
   - Sales enablement and process optimization
   - Revenue growth and business model optimization
   - Pricing strategies and value proposition development

4. Scaling & Investment:
   - Startup scaling and growth planning
   - Venture capital and funding strategies
   - Digital transformation consulting
   - Operational efficiency and process improvement

Provide strategic, actionable business development guidance with practical implementation steps.
"""

@tool
def business_dev_assistant(query: str) -> str:
    """
    Process business development queries with strategic guidance for technology companies.
    
    Args:
        query: A business development or growth strategy question
        
    Returns:
        Strategic business development guidance and recommendations
    """
    try:
        print("Routed to Business Dev Assistant")
        
        # Format query for the business dev agent
        formatted_query = f"Provide strategic business development guidance for: {query}"
        
        # Create business dev agent
        bizdev_agent = Agent(
            system_prompt=BUSINESS_DEV_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = bizdev_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the business development query."
            
    except Exception as e:
        return f"Business development error: {str(e)}"