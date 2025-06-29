from strands import Agent, tool
from web_browser_assistant import web_browser_assistant
import requests
import urllib.parse

LOUISIANA_LEGAL_SYSTEM_PROMPT = """
You are LouisianaLegalAssist, a specialized Louisiana business legal expert. Your role is to:

1. Business Formation & Compliance:
   - Louisiana business formation (LLC, Corporation, Partnership)
   - Louisiana Secretary of State requirements and filings
   - Louisiana business licensing and permits
   - Louisiana tax obligations and compliance

2. Business Operations:
   - Louisiana employment law for businesses
   - Louisiana commercial law and contracts
   - Louisiana real estate law for businesses
   - Louisiana regulatory compliance

3. Legal Procedures:
   - Louisiana court system and procedures
   - Louisiana business dissolution and bankruptcy
   - Legal documentation and filing requirements
   - Dispute resolution and litigation guidance

4. Resources & Guidance:
   - Current legal information with sources
   - Professional legal advice recommendations
   - Official Louisiana legal resources
   - Compliance checklists and requirements

Always provide current legal information with sources and disclaimers about seeking professional legal advice.
"""

@tool
def louisiana_legal_assistant(query: str) -> str:
    """
    Process Louisiana business legal queries with expert guidance and resources.
    
    Args:
        query: A Louisiana business legal question
        
    Returns:
        Louisiana legal guidance with sources and appropriate disclaimers
    """
    try:
        print("Routed to Louisiana Legal Assistant")
        
        # Get Louisiana-specific legal information
        legal_research = perform_louisiana_legal_research(query)
        
        # Format query for the Louisiana legal agent
        formatted_query = f"Provide comprehensive Louisiana legal guidance for: {query}\n\nResearch findings: {legal_research}"
        
        # Create Louisiana legal agent
        # Add web browsing for current data if needed

        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

            try:

                web_data = web_browser_assistant(f"Current research data: {query}")

                formatted_query += f"\n\nCurrent data from web: {web_data}"

            except:

                pass

        

        legal_agent = Agent(
            system_prompt=LOUISIANA_LEGAL_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = legal_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the Louisiana legal query."
            
    except Exception as e:
        return f"Louisiana legal guidance error: {str(e)}"

def perform_louisiana_legal_research(query):
    """Research Louisiana legal resources"""
    results = []
    
    # Louisiana Secretary of State resources
    try:
        sos_results = search_louisiana_sos(query)
        if sos_results:
            results.append(sos_results)
    except:
        pass
    
    # Legal resource guidance
    legal_guidance = get_louisiana_legal_resources(query)
    results.append(legal_guidance)
    
    return "\n\n".join(results)

def search_louisiana_sos(query):
    """Search Louisiana Secretary of State resources"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        if any(term in query.lower() for term in ['business', 'llc', 'corporation', 'filing']):
            sos_url = "https://www.sos.la.gov/BusinessServices/Pages/default.aspx"
            response = requests.get(sos_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return f"Louisiana Secretary of State Business Services: {sos_url}\nVerified accessible - contains business filing information and forms."
    except:
        pass
    
    return "Louisiana Secretary of State: sos.la.gov/BusinessServices"

def get_louisiana_legal_resources(query):
    """Provide Louisiana legal resource guidance"""
    return f"""Louisiana Legal Resources for '{query}':

OFFICIAL SOURCES:
- Louisiana Secretary of State: sos.la.gov
- Louisiana Legislature: legis.la.gov
- Louisiana Department of Revenue: revenue.louisiana.gov
- Louisiana Workforce Commission: laworks.net

LEGAL DATABASES:
- Louisiana State Bar Association: lsba.org
- Louisiana Supreme Court: lasc.org
- Louisiana Court of Appeal: lacoa.org

BUSINESS-SPECIFIC:
- Louisiana Economic Development: opportunitylouisiana.gov
- Louisiana Small Business Development Center: lsbdc.org

DISCLAIMER: This information is for educational purposes only and does not constitute legal advice. Consult with a qualified Louisiana attorney for specific legal matters."""