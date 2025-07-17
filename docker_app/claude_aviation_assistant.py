"""
Claude Aviation Assistant
Uses Claude 4.0 with proper tool handling for aviation queries
"""

from claude_tool_handler import AviationToolHandler, AVIATION_TOOLS
from typing import List, Dict, Any

# Aviation system prompt
AVIATION_SYSTEM_PROMPT = """
You are an aviation expert with access to real-time flight data.

You can use tools to:
1. Get current aircraft positions by registration number
2. Search for aircraft information by registration or name

For N-number queries (like N628TS): Use the get_flight_position tool.
For aircraft information queries: Use the search_aircraft tool.

Always provide comprehensive, accurate information about aircraft.
"""

class ClaudeAviationAssistant:
    """Aviation assistant using Claude 4.0 with proper tool handling"""
    
    def __init__(self, model_id="anthropic.claude-4-0:0"):
        self.model_id = model_id
        self.tool_handler = AviationToolHandler(model_id)
        self.tools = AVIATION_TOOLS
    
    def __call__(self, query: str) -> str:
        """Process aviation query with Claude and tools"""
        try:
            # Format initial messages
            messages = [
                {
                    "role": "system",
                    "content": AVIATION_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
            
            # Handle conversation with tools
            result = self.tool_handler.handle_conversation(messages, self.tools)
            
            # Check for errors
            if "error" in result:
                return f"Error: {result['error']}"
            
            # Extract final response
            response_message = result.get("response", {})
            content = response_message.get("content", [])
            
            # Convert content to string
            if isinstance(content, list):
                response_text = ""
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        response_text += item.get("text", "")
                    elif isinstance(item, str):
                        response_text += item
                return response_text
            elif isinstance(content, str):
                return content
            else:
                return str(content)
            
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Create global instance
claude_aviation_assistant = ClaudeAviationAssistant()

def aviation_assistant_claude(query: str) -> str:
    """Convenience function for Claude aviation assistant"""
    return claude_aviation_assistant(query)

# Example usage
if __name__ == "__main__":
    # Test the assistant
    query = "Where is N628TS now?"
    response = aviation_assistant_claude(query)
    print(f"Query: {query}")
    print(f"Response: {response}")