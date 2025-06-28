#!/usr/bin/env python3

from strands import Agent
from web_browser_assistant import web_browser_assistant

# Create a simple agent with just the web browser tool
agent = Agent(
    system_prompt="You are a web browsing assistant. Use the web_browser_assistant tool for any website-related queries.",
    tools=[web_browser_assistant]
)

# Test the agent
query = "browse infascination.com"
response = agent(query)
print("Agent Response:")
print(response)