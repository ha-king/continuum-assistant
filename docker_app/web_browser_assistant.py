from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
import requests
import urllib.parse
import json
import re

WEB_BROWSER_SYSTEM_PROMPT = """
You are WebBrowseAssist, a specialized web browsing assistant with real-time website access capabilities.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all research and responses. Never assume dates from model names or other sources.

Your role is to:

1. Website Analysis:
   - Browse and analyze websites in real-time
   - Extract company information and business intelligence
   - Identify services, products, and offerings
   - Analyze company positioning and value propositions

2. Content Extraction:
   - Parse website titles, descriptions, and headings
   - Extract contact information and business details
   - Summarize key business information
   - Identify target markets and specializations

3. Response Style:
   - Provide comprehensive analysis of website content
   - Focus on business intelligence and company offerings
   - Include specific details from website data
   - Present information in a structured, clear format

Always provide detailed analysis based on the actual website content provided to you.
"""

@tool
def web_browser_assistant(query: str) -> str:
    """
    Process and respond to web browsing queries with real-time website access.
    
    Args:
        query: A web browsing request or website analysis query
        
    Returns:
        Comprehensive website analysis and company intelligence
    """
    try:
        print("Routed to Web Browser Assistant")
        enhanced_query = enhance_query_with_realtime(query, "web")
        
        # Gather additional website intelligence
        company_intelligence = gather_company_intelligence(query)
        
        # Format query for the web browser agent
        formatted_query = f"Analyze this website data and provide comprehensive insights about the company's offerings and services: {enhanced_query}\n\nAdditional Website Data: {company_intelligence}"
        
        # Create web browser agent
        web_agent = Agent(
            system_prompt=WEB_BROWSER_SYSTEM_PROMPT,
            tools=[],  # No additional tools needed
        )
        
        agent_response = web_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to analyze the requested website."
            
    except Exception as e:
        return f"Web browsing error: {str(e)}\n\nAttempted to browse: {query}"

def gather_company_intelligence(query):
    """Actively gather comprehensive company intelligence"""
    company_info = extract_company_info(query)
    results = []
    
    for company_data in company_info:
        try:
            intelligence = fetch_company_intelligence(company_data)
            if intelligence:
                results.append(intelligence)
        except Exception as e:
            results.append(f"Company: {company_data.get('name', 'Unknown')}\nError: {str(e)}")
    
    return "\n\n".join(results) if results else "No company information found"

def extract_company_info(query):
    """Extract company information from query"""
    companies = []
    
    # Direct URL extraction
    urls = extract_urls_from_query(query)
    for url in urls:
        companies.append({
            'name': extract_domain_name(url),
            'website': url,
            'urls_to_check': [url]
        })
    
    # Special handling for infascination
    if 'infascination' in query.lower():
        companies.append({
            'name': 'Infascination LLC',
            'website': 'https://infascination.com',
            'urls_to_check': ['https://infascination.com']
        })
    
    return companies[:1]  # Limit to 1 company

def fetch_company_intelligence(company_data):
    """Fetch company intelligence"""
    intelligence = [f"=== COMPANY INTELLIGENCE: {company_data['name']} ==="]
    
    for url in company_data['urls_to_check']:
        try:
            page_content = fetch_website_content(url)
            if page_content and 'Error' not in page_content:
                intelligence.append(f"\n--- PAGE ANALYSIS: {url} ---")
                intelligence.append(page_content)
                break
        except:
            continue
    
    return "\n".join(intelligence)

def extract_domain_name(url):
    """Extract domain name from URL"""
    domain = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
    return domain.split('.')[0].title()

def extract_urls_from_query(query):
    """Extract URLs from query"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, query)
    
    domain_pattern = r'\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b'
    domains = re.findall(domain_pattern, query)
    
    for domain in domains:
        if not domain.startswith('http'):
            urls.append(f"https://{domain}")
    
    return list(set(urls))

def fetch_website_content(url):
    """Fetch website content"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return analyze_webpage_content(response, url)
        else:
            return f"HTTP Status: {response.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_webpage_content(response, url):
    """Analyze webpage content"""
    content = response.text
    analysis = []
    
    analysis.append(f"URL: {url}")
    analysis.append(f"Status: {response.status_code}")
    
    # Extract title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        analysis.append(f"Title: {title}")
    
    # Extract meta description
    meta_desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if meta_desc_match:
        description = meta_desc_match.group(1).strip()
        analysis.append(f"Description: {description}")
    
    # Extract headings
    headings = []
    for level in range(1, 4):
        heading_pattern = f'<h{level}[^>]*>(.*?)</h{level}>'
        matches = re.findall(heading_pattern, content, re.IGNORECASE | re.DOTALL)
        for match in matches[:2]:
            clean_heading = re.sub(r'<[^>]+>', '', match).strip()
            if clean_heading and len(clean_heading) < 100:
                headings.append(f"H{level}: {clean_heading}")
    
    if headings:
        analysis.append(f"Headings: {'; '.join(headings[:3])}")
    
    from datetime import datetime
    analysis.append(f"Accessed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    return "\n".join(analysis)