from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
import requests

COMPANY_INTELLIGENCE_SYSTEM_PROMPT = """
You are CompanyIntelligenceAssist, a specialized assistant for competitive analysis and business intelligence.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all research and responses.

Your role is to:

1. Competitive Analysis:
   - Market positioning research
   - Competitor product/service analysis
   - Pricing strategy research
   - Market share analysis

2. Business Intelligence:
   - Industry trend analysis
   - Financial performance research
   - Strategic partnership identification
   - Market opportunity assessment

3. Due Diligence:
   - Company background research
   - Leadership team analysis
   - Financial health assessment
   - Risk factor identification

Focus on publicly available information and ethical research practices.
"""

@tool
def company_intelligence_assistant(query: str) -> str:
    """
    Provide competitive analysis and business intelligence research.
    
    Args:
        query: A company intelligence research request
        
    Returns:
        Business intelligence analysis with sources
    """
    try:
        print("Routed to Company Intelligence Assistant")
        enhanced_query = enhance_query_with_realtime(query, "company_intelligence")

        
        intelligence_data = gather_company_intelligence(query)
        
        formatted_query = f"Analyze company intelligence: {query}\n\nIntelligence Data: {intelligence_data}"
        
        intelligence_agent = Agent(
            system_prompt=COMPANY_INTELLIGENCE_SYSTEM_PROMPT,
            tools=[],
        )
        
        response = intelligence_agent(formatted_query)
        return str(response)
        
    except Exception as e:
        return f"Company intelligence error: {str(e)}"

def gather_company_intelligence(query):
    """Gather company intelligence from public sources"""
    company_name = extract_company_name(query)
    
    intelligence_sources = f"""COMPANY INTELLIGENCE SOURCES: {company_name}

Financial Information:
- SEC filings (if public company)
- Annual reports and 10-K forms
- Quarterly earnings reports
- Credit rating agencies

Market Research:
- Industry reports and analysis
- Market research firms (IBISWorld, etc.)
- Trade publications
- Industry association reports

Competitive Analysis:
- Company websites and marketing materials
- Press releases and news coverage
- Social media presence analysis
- Customer reviews and feedback

Leadership Intelligence:
- Executive team backgrounds
- Board of directors information
- Key personnel changes
- Leadership interviews and speeches

Strategic Intelligence:
- Partnership announcements
- Merger and acquisition activity
- Patent filings and IP portfolio
- Expansion plans and investments

Recommended Research Tools:
- Google Alerts for company mentions
- LinkedIn for personnel changes
- Crunchbase for funding information
- PitchBook for private company data
- Industry-specific databases"""
    
    return intelligence_sources

def extract_company_name(query):
    """Extract company name from intelligence query"""
    # Remove common phrases
    clean_query = query.lower()
    for phrase in ['intelligence on', 'research on', 'analysis of', 'information about']:
        clean_query = clean_query.replace(phrase, '')
    return clean_query.strip().title()