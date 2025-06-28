#!/usr/bin/env python3
import sys
sys.path.append('/home/ubuntu/.venv/lib/python3.12/site-packages')

from strands import Agent
from web_browser_assistant import web_browser_assistant

# Test web browser through strands agent
agent = Agent(
    system_prompt="Use web_browser_assistant for website queries",
    tools=[web_browser_assistant]
)

query = "browse infascination.com"
print("Testing web browser via strands agent...")
try:
    response = agent(query)
    print("SUCCESS:", str(response)[:200] + "...")
except Exception as e:
    print("ERROR:", str(e))