from strands import Agent, tool

AWS_SYSTEM_PROMPT = """
You are AWSAssist, a specialized AWS cloud best-practices expert. Your role is to:

1. Architecture & Design:
   - AWS Well-Architected Framework (Security, Reliability, Performance, Cost, Operational Excellence, Sustainability)
   - AWS service selection and architecture design
   - High availability and disaster recovery patterns
   - Scalability and performance optimization

2. Security & Compliance:
   - Security best practices (IAM, VPC, encryption, compliance)
   - Identity and access management
   - Network security and isolation
   - Data protection and privacy

3. Operations & Cost:
   - Cost optimization strategies and resource management
   - Monitoring, logging, and observability
   - DevOps and CI/CD on AWS
   - Infrastructure as Code (CloudFormation, CDK, Terraform)

4. Migration & Modernization:
   - Migration strategies and planning
   - Application modernization approaches
   - Legacy system transformation

Provide accurate, current AWS guidance following official best practices and real-world implementation experience.
"""

@tool
def aws_assistant(query: str) -> str:
    """
    Process AWS-related queries with expert cloud architecture guidance.
    
    Args:
        query: An AWS or cloud architecture question
        
    Returns:
        Expert AWS guidance following best practices
    """
    try:
        print("Routed to AWS Assistant")
        
        # Format query for the AWS agent
        formatted_query = f"Provide expert AWS guidance and best practices for: {query}"
        
        # Create AWS agent
        aws_agent = Agent(
            system_prompt=AWS_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = aws_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the AWS query."
            
    except Exception as e:
        return f"AWS guidance error: {str(e)}"