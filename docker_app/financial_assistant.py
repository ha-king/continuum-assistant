from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime

FINANCIAL_SYSTEM_PROMPT = """
You are FinancialAssist, a specialized financial records and reports expert. Your role is to:

1. Financial Analysis:
   - Financial statement analysis (income statements, balance sheets, cash flow)
   - Financial ratios and metrics interpretation
   - Investment analysis and valuation
   - Performance measurement and benchmarking

2. Accounting Expertise:
   - Accounting principles and standards (GAAP, IFRS)
   - Tax reporting and compliance guidance
   - Audit procedures and internal controls
   - Cost accounting and management accounting

3. Planning & Strategy:
   - Budgeting and forecasting
   - Financial planning and modeling
   - Risk assessment and management
   - Capital structure optimization

Provide accurate, professional financial guidance with clear explanations and practical applications.
"""

@tool
def financial_assistant(query: str) -> str:
    """
    Process financial queries with expert analysis and guidance.
    
    Args:
        query: A financial question or analysis request
        
    Returns:
        Professional financial guidance and analysis
    """
    try:
        print("Routed to Financial Assistant")
        enhanced_query = enhance_query_with_realtime(query, "financial")
        
        # Format query for the financial agent
        formatted_query = f"Provide expert financial analysis and guidance for: {enhanced_query}"
        
        financial_agent = Agent(
            system_prompt=FINANCIAL_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = financial_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the financial query."
            
    except Exception as e:
        return f"Financial analysis error: {str(e)}"