from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
import requests
import re

BUSINESS_CONTACT_SYSTEM_PROMPT = """
You are BusinessContactAssist, a specialized assistant for finding legitimate business contact information.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all research and responses.

Your role is to:

1. Business Contact Research:
   - Find official company contact information
   - Locate business phone numbers and addresses
   - Identify customer service and sales contacts
   - Research corporate headquarters information

2. Professional Networking:
   - Find LinkedIn company pages
   - Identify key business executives (publicly available)
   - Locate press contacts and media relations
   - Find investor relations contacts

3. Compliance:
   - Only use publicly available business information
   - Focus on official company channels
   - Respect privacy and data protection laws
   - Provide sources for all contact information

Always verify information through official business channels and provide sources.
"""

@tool
def business_contact_assistant(query: str) -> str:
    """
    Find legitimate business contact information for companies and organizations.
    
    Args:
        query: A business contact research request
        
    Returns:
        Business contact information with sources
    """
    try:
        print("Routed to Business Contact Assistant")
        enhanced_query = enhance_query_with_realtime(query, "business_contact")

        
        contact_data = gather_business_contacts(query)
        
        formatted_query = f"Find business contact information: {query}\n\nBusiness Data: {contact_data}"
        
        contact_agent = Agent(
            system_prompt=BUSINESS_CONTACT_SYSTEM_PROMPT,
            tools=[],
        )
        
        response = contact_agent(formatted_query)
        return str(response)
        
    except Exception as e:
        return f"Business contact research error: {str(e)}"

def gather_business_contacts(query):
    """Gather business contact information from public sources"""
    results = []
    
    company_name = extract_company_name(query)
    
    # Search for official website
    website_info = find_company_website(company_name)
    if website_info:
        results.append(website_info)
    
    # Search for business directory listings
    directory_info = search_business_directories(company_name)
    if directory_info:
        results.append(directory_info)
    
    return "\n\n".join(results) if results else f"No business contact information found for {company_name}"

def extract_company_name(query):
    """Extract company name from query"""
    # Remove common phrases
    clean_query = query.lower()
    for phrase in ['contact information for', 'find contacts for', 'business contacts for']:
        clean_query = clean_query.replace(phrase, '')
    return clean_query.strip().title()

def find_company_website(company_name):
    """Find company website and contact information"""
    try:
        # Try common domain patterns
        domains = [
            f"https://{company_name.lower().replace(' ', '')}.com",
            f"https://www.{company_name.lower().replace(' ', '')}.com"
        ]
        
        for domain in domains:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(domain, headers=headers, timeout=10)
                if response.status_code == 200:
                    return f"Official Website: {domain}\nStatus: Accessible\nNote: Check contact/about pages for business contact information"
            except:
                continue
                
    except:
        pass
    
    return f"Website Search: Unable to locate official website for {company_name}"

def search_business_directories(company_name):
    """Search business directories for contact information"""
    return f"""Business Directory Search: {company_name}

Recommended Sources:
1. Better Business Bureau (bbb.org)
2. Google Business Listings
3. Yelp Business Pages
4. LinkedIn Company Pages
5. Industry-specific directories
6. Chamber of Commerce listings

Note: Verify all contact information through official company channels."""