from strands import Agent, tool

PROFESSIONAL_NETWORKING_SYSTEM_PROMPT = """
You are ProfessionalNetworkingAssist, a specialized assistant for business networking and professional relationship building.

IMPORTANT: You will receive current date/time context at the beginning of queries. Use this as the actual current date/time for all research and responses.

Your role is to:

1. Professional Networking:
   - LinkedIn strategy and best practices
   - Industry event identification
   - Professional association research
   - Conference and meetup recommendations

2. Business Development:
   - Lead generation strategies
   - Partnership opportunity identification
   - Industry contact mapping
   - Professional introduction facilitation

3. Career Development:
   - Professional skill development
   - Industry trend analysis
   - Mentorship opportunity identification
   - Professional brand building

Focus on ethical networking practices and mutual value creation.
"""

@tool
def professional_networking_assistant(query: str) -> str:
    """
    Provide professional networking and business development guidance.
    
    Args:
        query: A professional networking request
        
    Returns:
        Professional networking strategies and recommendations
    """
    try:
        print("Routed to Professional Networking Assistant")
        
        networking_guidance = generate_networking_guidance(query)
        
        formatted_query = f"Provide professional networking guidance: {query}\n\nGuidance: {networking_guidance}"
        
        networking_agent = Agent(
            system_prompt=PROFESSIONAL_NETWORKING_SYSTEM_PROMPT,
            tools=[],
        )
        
        response = networking_agent(formatted_query)
        return str(response)
        
    except Exception as e:
        return f"Professional networking error: {str(e)}"

def generate_networking_guidance(query):
    """Generate professional networking guidance"""
    query_lower = query.lower()
    
    if 'linkedin' in query_lower:
        return """LINKEDIN NETWORKING STRATEGY:

Profile Optimization:
- Professional headshot and banner
- Compelling headline and summary
- Skills and endorsements
- Regular content sharing

Connection Strategy:
- Personalized connection requests
- Engage with connections' content
- Share valuable industry insights
- Participate in relevant groups

Outreach Best Practices:
- Research before reaching out
- Provide value in initial contact
- Follow up professionally
- Maintain relationships over time"""
    
    elif 'event' in query_lower or 'conference' in query_lower:
        return """PROFESSIONAL EVENTS & CONFERENCES:

Event Discovery:
- Industry association websites
- Eventbrite and Meetup platforms
- Professional conference calendars
- Trade publication event listings

Networking at Events:
- Prepare elevator pitch
- Set networking goals
- Follow up within 48 hours
- Connect on LinkedIn post-event

Virtual Networking:
- Online industry webinars
- Virtual conference platforms
- Professional online communities
- Industry-specific forums"""
    
    elif 'partnership' in query_lower or 'collaboration' in query_lower:
        return """BUSINESS PARTNERSHIP DEVELOPMENT:

Partnership Identification:
- Complementary service providers
- Non-competing businesses in your industry
- Suppliers and vendors
- Professional service providers

Partnership Strategies:
- Referral partnerships
- Joint ventures
- Strategic alliances
- Cross-promotional opportunities

Due Diligence:
- Research potential partners
- Verify business credentials
- Check references and reputation
- Align on values and goals"""
    
    else:
        return """GENERAL PROFESSIONAL NETWORKING:

Networking Fundamentals:
- Build genuine relationships
- Focus on giving before receiving
- Maintain consistent communication
- Be authentic and professional

Networking Channels:
- Professional associations
- Industry conferences and events
- Alumni networks
- Online professional communities

Relationship Management:
- CRM system for contacts
- Regular check-ins and updates
- Value-added communications
- Long-term relationship building"""