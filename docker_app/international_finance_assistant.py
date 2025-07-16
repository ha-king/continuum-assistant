from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime

INTERNATIONAL_FINANCE_SYSTEM_PROMPT = """
You are InternationalFinanceExpert, a specialized assistant for global finance and international monetary systems.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all analysis and responses.

Your expertise includes:

1. International Finance:
   - Foreign exchange markets and currency analysis
   - Cross-border capital flows and investments
   - International banking and payment systems
   - Sovereign debt and credit risk analysis

2. Global Monetary Policy:
   - Central bank policies and coordination
   - Interest rate differentials and carry trades
   - Quantitative easing and monetary stimulus
   - Currency intervention and stabilization

3. International Trade Finance:
   - Trade financing mechanisms and instruments
   - Export credit and guarantee programs
   - Documentary credits and collections
   - Supply chain financing solutions

4. Emerging Markets:
   - Developing economy financial systems
   - Capital market development and access
   - Foreign direct investment flows
   - Financial inclusion and fintech adoption

Provide data-driven analysis with consideration of regulatory frameworks and market dynamics.
"""

@tool
def international_finance_assistant(query: str) -> str:
    """
    Provide international finance analysis and global monetary expertise.
    
    Args:
        query: An international finance analysis request
        
    Returns:
        Comprehensive international finance analysis and insights
    """
    try:
        print("Routed to International Finance Assistant")
        enhanced_query = enhance_query_with_realtime(query, "international_finance")

        
        finance_framework = generate_finance_framework(query)
        
        formatted_query = f"Provide international finance analysis: {query}\n\nFinance Framework: {finance_framework}"
        
        finance_agent = Agent(
            system_prompt=INTERNATIONAL_FINANCE_SYSTEM_PROMPT,
            tools=[],
        )
        
        response = finance_agent(formatted_query)
        return str(response)
        
    except Exception as e:
        return f"International finance analysis error: {str(e)}"

def generate_finance_framework(query):
    """Generate international finance analysis framework"""
    query_lower = query.lower()
    
    if any(term in query_lower for term in ['currency', 'forex', 'exchange rate']):
        return """FOREIGN EXCHANGE ANALYSIS FRAMEWORK:

Currency Fundamentals:
- Interest rate differentials and yield curves
- Inflation rates and purchasing power parity
- Current account and trade balances
- Political stability and policy credibility

Market Dynamics:
- Central bank intervention and reserves
- Carry trade flows and risk appetite
- Technical analysis and momentum factors
- Volatility patterns and correlations

Major Currency Pairs:
- USD strength and dollar index trends
- EUR dynamics and ECB policy impacts
- JPY safe-haven flows and BoJ intervention
- GBP Brexit and UK economic impacts
- CNY internationalization and capital controls"""
    
    elif any(term in query_lower for term in ['emerging markets', 'developing', 'brics']):
        return """EMERGING MARKETS FINANCE FRAMEWORK:

Capital Flow Analysis:
- Foreign direct investment trends
- Portfolio investment volatility
- Debt sustainability and external financing
- Reserve adequacy and liquidity buffers

Risk Assessment:
- Country risk ratings and sovereign spreads
- Currency crisis indicators and early warning
- Banking system stability and supervision
- Corporate debt levels and foreign currency exposure

Development Finance:
- Multilateral development bank lending
- Blended finance and impact investing
- Financial inclusion and digital payments
- Green finance and climate adaptation funding"""
    
    elif any(term in query_lower for term in ['central bank', 'monetary policy', 'fed']):
        return """CENTRAL BANK POLICY ANALYSIS FRAMEWORK:

Policy Tools and Transmission:
- Interest rate policy and forward guidance
- Quantitative easing and asset purchases
- Reserve requirements and liquidity provision
- Macroprudential measures and financial stability

International Coordination:
- G7/G20 policy coordination mechanisms
- Currency swap arrangements and facilities
- Basel III implementation and capital standards
- Cross-border regulatory cooperation

Market Impact Assessment:
- Bond yield curve effects and term structure
- Equity market valuations and risk premiums
- Credit spreads and corporate financing costs
- Currency impacts and international spillovers"""
    
    else:
        return """GENERAL INTERNATIONAL FINANCE FRAMEWORK:

Global Financial System:
- International payment and settlement systems
- Cross-border banking and correspondent relationships
- Financial market infrastructure and connectivity
- Regulatory harmonization and standards

Risk Management:
- Country and sovereign risk assessment
- Currency hedging strategies and instruments
- Political risk insurance and guarantees
- Operational risk in cross-border transactions

Market Analysis:
- Global liquidity conditions and flows
- International bond and equity market trends
- Commodity financing and trade credit
- Fintech innovation and digital currencies"""