"""
Fix for tool_use/tool_result validation error in Claude 3.5 Sonnet
"""

import json
import boto3
import uuid

def format_tool_result(tool_use_id, result):
    """Format tool result in the correct format for Claude"""
    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": result
    }

def handle_conversation_with_tools(messages, tools):
    """Handle a conversation with tools properly"""
    bedrock = boto3.client('bedrock-runtime')
    
    # Initial request
    response = bedrock.converse_stream(
        modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
        messages=messages,
        tools=tools
    )
    
    # Process the streaming response
    tool_use_id = None
    tool_name = None
    tool_params = None
    
    for event in response['stream']:
        if 'message' in event:
            message = event['message']
            
            # Check for tool_use
            if message.get('type') == 'tool_use':
                tool_use_id = message.get('id')
                tool_name = message.get('name')
                tool_params = message.get('input', {})
                
                # Execute the tool (simplified example)
                tool_result = execute_tool(tool_name, tool_params)
                
                # Format the tool result correctly
                tool_result_message = format_tool_result(tool_use_id, tool_result)
                
                # Continue the conversation with the tool result
                messages.append({"role": "assistant", "content": [{"type": "tool_use", "id": tool_use_id, "name": tool_name, "input": tool_params}]})
                messages.append({"role": "user", "content": [tool_result_message]})
                
                # Make a new request with the updated messages
                return handle_conversation_with_tools(messages, tools)
            
            # Process normal content
            if message.get('type') == 'content':
                print(message.get('text', ''), end='', flush=True)
    
    return messages

def execute_tool(tool_name, params):
    """Execute a tool and return the result"""
    # Implement your tool execution logic here
    if tool_name == "get_weather":
        return {"temperature": 72, "condition": "sunny"}
    elif tool_name == "search_web":
        return {"results": ["Result 1", "Result 2"]}
    else:
        return {"error": "Tool not found"}

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
    
    # Initial messages
    messages = [
        {"role": "user", "content": "What's the weather in Seattle?"}
    ]
    
    # Handle conversation
    handle_conversation_with_tools(messages, tools)