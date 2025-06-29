from strands import Agent, tool
from web_browser_assistant import web_browser_assistant

CRYPTOGRAPHY_SYSTEM_PROMPT = """
You are CryptographyAssist, a specialized cryptography expert. Your role is to:

1. Cryptographic Algorithms:
   - Symmetric and asymmetric encryption
   - Hash functions and digital signatures
   - Key exchange protocols
   - Cryptographic primitives

2. Applied Cryptography:
   - SSL/TLS protocols
   - Public key infrastructure (PKI)
   - Cryptographic implementations
   - Security protocol design

3. Modern Cryptography:
   - Post-quantum cryptography
   - Zero-knowledge proofs
   - Homomorphic encryption
   - Elliptic curve cryptography

Provide technical cryptographic guidance with security best practices and implementation considerations.
"""

@tool
def cryptography_assistant(query: str) -> str:
    """
    Process cryptography-related queries with expert technical guidance.
    
    Args:
        query: A cryptography question or technical request
        
    Returns:
        Expert cryptographic guidance and technical analysis
    """
    try:
        print("Routed to Cryptography Assistant")
        
        formatted_query = f"Provide expert cryptographic analysis and guidance for: {query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        crypto_agent = Agent(
            system_prompt=CRYPTOGRAPHY_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = crypto_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the cryptography query."
            
    except Exception as e:
        return f"Cryptography analysis error: {str(e)}"