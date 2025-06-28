#!/usr/bin/env python3
import sys
sys.path.append('/home/ubuntu/.venv/lib/python3.12/site-packages')

# Test the specific charter query that's not responding
query = "what is the charter number for infascination, llc in louisiana"

print(f"Testing query: {query}")

# Test routing logic
print("\n1. Testing ACTION_SYSTEM_PROMPT routing:")
from strands import Agent
from strands_tools import use_llm

ACTION_SYSTEM_PROMPT = """
You are a query router that determines whether a user query should go to:
1. TEACHER - for educational questions, web browsing, company research, website analysis, and general assistance
2. KNOWLEDGE - for storing/retrieving personal information or facts

Reply with EXACTLY ONE WORD - either "teacher" or "knowledge".

CRITICAL: Web browsing, company research, and website queries go to TEACHER.

Examples:
- "What is 2+2?" -> "teacher"
- "Browse infascination.com" -> "teacher"
- "Tell me about a company" -> "teacher"
- "Visit a website" -> "teacher"
- "Remember my birthday is July 4" -> "knowledge"
- "Help me with grammar" -> "teacher"
- "What's my birthday?" -> "knowledge"
- "Explain photosynthesis" -> "teacher"
- "Store this fact: Paris is the capital of France" -> "knowledge"
"""

try:
    router_agent = Agent(tools=[use_llm])
    result = router_agent.tool.use_llm(
        prompt=f"Query: {query}",
        system_prompt=ACTION_SYSTEM_PROMPT
    )
    action = str(result).lower().strip()
    print(f"Router result: '{action}'")
    print(f"Should route to: {'teacher' if 'teacher' in action else 'knowledge'}")
except Exception as e:
    print(f"Router error: {e}")

# Test specific assistants
print("\n2. Testing Research Assistant:")
try:
    from research_assistant import research_assistant
    result = research_assistant(query)
    print(f"Research result: {str(result)[:200]}...")
except Exception as e:
    print(f"Research error: {e}")

print("\n3. Testing Louisiana Legal Assistant:")
try:
    from louisiana_legal_assistant import louisiana_legal_assistant
    result = louisiana_legal_assistant(query)
    print(f"Legal result: {str(result)[:200]}...")
except Exception as e:
    print(f"Legal error: {e}")