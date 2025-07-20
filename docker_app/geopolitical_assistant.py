from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime

GEOPOLITICAL_SYSTEM_PROMPT = """
You are GeopoliticalExpert, a specialized assistant for geopolitical analysis and international relations.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all analysis and responses.

Your expertise includes:

1. Geopolitical Analysis:
   - International relations and diplomacy
   - Regional conflicts and tensions
   - Trade wars and economic sanctions
   - Military alliances and security arrangements

2. Global Risk Assessment:
   - Political stability analysis
   - Election impact assessments
   - Regulatory and policy changes
   - Cross-border investment risks

3. Strategic Intelligence:
   - Supply chain geopolitical risks
   - Energy security and resources
   - Technology transfer restrictions
   - International law and treaties

Provide balanced, fact-based analysis with multiple perspectives on complex geopolitical issues.
"""

@tool
def geopolitical_assistant(query: str) -> str:
    """
    Provide geopolitical analysis and international relations expertise.
    
    Args:
        query: A geopolitical analysis request
        
    Returns:
        Comprehensive geopolitical analysis and insights
    """
    try:
        print("Routed to Geopolitical Assistant")
        enhanced_query = enhance_query_with_realtime(query, "geopolitical")

        
        analysis_framework = generate_geopolitical_framework(query)
        
        formatted_query = f"Provide geopolitical analysis: {query}\n\nAnalysis Framework: {analysis_framework}"
        
        geopolitical_agent = Agent(
            system_prompt=GEOPOLITICAL_SYSTEM_PROMPT,
            tools=[],
        )
        
        response = geopolitical_agent(formatted_query)
        return str(response)
        
    except Exception as e:
        return f"Geopolitical analysis error: {str(e)}"

def generate_geopolitical_framework(query):
    """Generate geopolitical analysis framework"""
    query_lower = query.lower()
    
    if any(term in query_lower for term in ['china', 'us-china', 'trade war']):
        return """US-CHINA RELATIONS ANALYSIS FRAMEWORK:

Key Areas:
- Trade and economic relations
- Technology competition and restrictions
- Military presence in South China Sea
- Taiwan situation and cross-strait relations
- Supply chain dependencies and decoupling

Economic Implications:
- Tariff impacts on global trade
- Technology transfer restrictions
- Investment screening mechanisms
- Currency and monetary policy effects

Strategic Considerations:
- Alliance building (QUAD, AUKUS)
- Belt and Road Initiative impacts
- Semiconductor and critical technology competition
- Climate cooperation vs. competition"""
    
    elif any(term in query_lower for term in ['russia', 'ukraine', 'nato']):
        return """RUSSIA-UKRAINE-NATO ANALYSIS FRAMEWORK:

Conflict Dynamics:
- Military operations and territorial control
- International sanctions and economic warfare
- Energy security and supply disruptions
- Humanitarian and refugee impacts

Geopolitical Implications:
- NATO expansion and Article 5 considerations
- European security architecture changes
- Nuclear deterrence and escalation risks
- Global food security impacts

Economic Consequences:
- Energy market disruptions
- Commodity price volatility
- Financial system fragmentation
- Reconstruction and recovery planning"""
    
    elif any(term in query_lower for term in ['middle east', 'israel', 'iran', 'saudi']):
        return """MIDDLE EAST ANALYSIS FRAMEWORK:

Regional Dynamics:
- Israeli-Palestinian conflict developments
- Iran nuclear program and sanctions
- Saudi-Iran regional competition
- Gulf Cooperation Council relations

Energy Geopolitics:
- Oil production and OPEC+ decisions
- Energy transition impacts on petrostates
- Strategic petroleum reserves
- Alternative energy partnerships

Security Considerations:
- Regional proxy conflicts
- Maritime security in key straits
- Terrorism and counterterrorism
- Arms sales and military partnerships"""
    
    else:
        return """GENERAL GEOPOLITICAL ANALYSIS FRAMEWORK:

Political Risk Factors:
- Government stability and transitions
- Electoral processes and outcomes
- Policy continuity and changes
- International agreement compliance

Economic Security:
- Trade relationship dependencies
- Critical supply chain vulnerabilities
- Currency stability and controls
- Investment protection mechanisms

Strategic Considerations:
- Alliance structures and partnerships
- Military capabilities and deployments
- Diplomatic engagement levels
- Multilateral institution participation"""