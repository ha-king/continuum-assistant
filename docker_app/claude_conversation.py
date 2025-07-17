"""
Claude 4.0 Conversation Handler with Proper Tool Usage
"""

import boto3
import json
from typing import Dict, List, Any, Optional

class ClaudeConversation:
    """Handles conversations with Claude 4.0 with proper tool usage"""
    
    def __init__(self, model_id="anthropic.claude-4-0:0"):
        """Initialize with Claude 4.0 by default"""
        self.model_id = model_id
        self.bedrock = boto3.client('bedrock-runtime')
        self.messages = []
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation"""
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation"""
        self.messages.append({"role": "assistant", "content": content})
    
    def converse(self, tools: Optional[List[Dict]] = None) -> str:
        """Handle a complete conversation with tools"""
        try:
            # Make initial request
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=self.messages,
                tools=tools
            )
            
            # Get the response message
            response_message = response.get('messages', [])[-1]
            content = response_message.get('content', '')
            
            # Check if tool use was requested
            if 'tool_use' in str(response_message):
                # Extract tool use details
                tool_calls = self._extract_tool_calls(response_message)
                
                # Add the assistant's tool request to conversation
                self.messages.append(response_message)
                
                # For each tool call, execute and add results
                for tool_call in tool_calls:
                    tool_use_id = tool_call.get('id')
                    tool_name = tool_call.get('name')
                    tool_params = tool_call.get('input', {})
                    
                    # Execute the tool
                    tool_result = self._execute_tool(tool_name, tool_params)
                    
                    # Format the tool result correctly
                    tool_result_message = {
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": tool_result
                        }]
                    }
                    
                    # Add tool result to conversation
                    self.messages.append(tool_result_message)
                
                # Continue the conversation with the tool results
                return self.converse(tools)
            else:
                # Add the response to conversation history
                self.messages.append(response_message)
                return content
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _extract_tool_calls(self, message: Dict) -> List[Dict]:
        """Extract tool calls from a message"""
        tool_calls = []
        
        # Handle different message formats
        if isinstance(message.get('content'), list):
            for item in message['content']:
                if item.get('type') == 'tool_use':
                    tool_calls.append(item)
        elif isinstance(message.get('content'), str):
            # Parse tool calls from content string if needed
            pass
        
        return tool_calls
    
    def _execute_tool(self, tool_name: str, params: Dict) -> Dict:
        """Execute a tool and return the result"""
        # Implement your tool execution logic here
        # This is where you would call your actual tools
        
        if tool_name == "get_weather":
            return {"temperature": 72, "condition": "sunny"}
        elif tool_name == "search_web":
            return {"results": ["Result 1", "Result 2"]}
        else:
            return {"error": f"Tool {tool_name} not found"}

# Example usage
if __name__ == "__main__":
    # Define tools
    tools = [
        {
            "name": "get_weather",
            "description": "Get the current weather",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        }
    ]
    
    # Create conversation
    conversation = ClaudeConversation()
    
    # Add user message
    conversation.add_user_message("What's the weather in Seattle?")
    
    # Get response
    response = conversation.converse(tools)
    print(response)