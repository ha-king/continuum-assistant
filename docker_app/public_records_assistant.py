from strands import Agent, tool

PUBLIC_RECORDS_SYSTEM_PROMPT = """
You are PublicRecordsAssist, a specialized assistant for public records research and legal compliance.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all research and responses.

Your role is to:

1. Public Records Research:
   - Guide users to official government databases
   - Explain public record access procedures
   - Identify relevant regulatory filings
   - Provide courthouse and agency contact information

2. Legal Compliance:
   - Business registration verification
   - Professional license lookups
   - Corporate filing research
   - Regulatory compliance checks

3. Due Diligence:
   - Background check guidance for employers
   - Property record research
   - Court record access procedures
   - Professional credential verification

Always direct users to official government sources and explain proper legal procedures.
"""

@tool
def public_records_assistant(query: str) -> str:
    """
    Provide guidance on accessing public records for legal compliance purposes.
    
    Args:
        query: A public records research request
        
    Returns:
        Public records research guidance with official sources
    """
    try:
        print("Routed to Public Records Assistant")
        
        records_guidance = generate_records_guidance(query)
        
        formatted_query = f"Provide public records research guidance: {query}\n\nGuidance: {records_guidance}"
        
        records_agent = Agent(
            system_prompt=PUBLIC_RECORDS_SYSTEM_PROMPT,
            tools=[],
        )
        
        response = records_agent(formatted_query)
        return str(response)
        
    except Exception as e:
        return f"Public records research error: {str(e)}"

def generate_records_guidance(query):
    """Generate guidance for public records research"""
    query_lower = query.lower()
    
    if 'business' in query_lower or 'company' in query_lower:
        return """BUSINESS RECORDS RESEARCH:

Secretary of State Databases:
- Corporate registrations and filings
- Business license information
- Registered agent details
- Annual report filings

Federal Resources:
- SEC EDGAR database (sec.gov/edgar)
- USPTO trademark/patent search
- IRS tax-exempt organization search

State Resources:
- State-specific business databases
- Professional licensing boards
- Workers' compensation records
- Unemployment insurance records"""
    
    elif 'property' in query_lower or 'real estate' in query_lower:
        return """PROPERTY RECORDS RESEARCH:

County Resources:
- Assessor's office records
- Deed and title records
- Property tax information
- Zoning and permit records

Online Databases:
- County clerk websites
- Property appraiser sites
- GIS mapping systems
- Tax collector databases"""
    
    elif 'court' in query_lower or 'legal' in query_lower:
        return """COURT RECORDS RESEARCH:

Federal Courts:
- PACER system (pacer.gov)
- Federal case filings
- Bankruptcy records
- Appeals court decisions

State/Local Courts:
- County clerk offices
- State court databases
- Municipal court records
- Traffic court filings

Note: Some records may require fees or in-person requests."""
    
    else:
        return """GENERAL PUBLIC RECORDS GUIDANCE:

Government Resources:
- Federal: usa.gov
- State: Individual state .gov sites
- Local: City/county websites
- FOIA requests for federal agencies

Common Record Types:
- Business registrations
- Property records
- Court filings
- Professional licenses
- Vital records (birth/death/marriage)

Access Methods:
- Online databases
- In-person requests
- Written requests
- Freedom of Information Act requests"""