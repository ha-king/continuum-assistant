"""
Claude Tool Handler
Properly handles tool use/tool result for Claude models
"""

import boto3
import json
from typing import Dict, List, Any, Optional

class ClaudeToolHandler:
    """Handles Claude tool usage with proper tool_use/tool_result format"""
    
    def __init__(self, model_id="anthropic.claude-4-0:0"):
        """Initialize with Claude 4.0 by default"""
        self.model_id = model_id
        self.bedrock = boto3.client('bedrock-runtime')
    
    def handle_conversation(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
        """Handle a complete conversation with tools"""
        try:
            # Validate and fix conversation history before making request
            messages = self._validate_conversation_history(messages)
            
            # Make initial request
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=messages,
                tools=tools
            )
            
            # Get the response message
            response_message = response.get('message', {})
            
            # Check if tool use was requested
            if self._has_tool_use(response_message):
                # Extract tool use details
                tool_calls = self._extract_tool_calls(response_message)
                
                # Add the assistant's tool request to conversation
                messages.append({"role": "assistant", "content": response_message.get('content', [])})
                
                # Track tool_use_ids for this turn to ensure we don't create orphaned tool_results
                current_tool_use_ids = set()
                for tool_call in tool_calls:
                    current_tool_use_ids.add(tool_call.get('id'))
                
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
                    messages.append(tool_result_message)
                
                # Continue the conversation with the tool results
                return self.handle_conversation(messages, tools)
            else:
                # Add the response to conversation history if it's not already there
                if not messages or messages[-1].get('role') != 'assistant':
                    messages.append({"role": "assistant", "content": response_message.get('content', [])})
                
                return {
                    "messages": messages,
                    "response": response_message
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "messages": messages
            }
    
    def _has_tool_use(self, message: Dict) -> bool:
        """Check if message contains tool use"""
        content = message.get('content', [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    return True
        return False
    
    def _extract_tool_calls(self, message: Dict) -> List[Dict]:
        """Extract tool calls from a message"""
        tool_calls = []
        content = message.get('content', [])
        
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    tool_calls.append(item)
        
        return tool_calls
    
    def _validate_conversation_history(self, messages: List[Dict]) -> List[Dict]:
        """Validate and fix conversation history to prevent ValidationException"""
        if not messages:
            return messages
            
        # Collect all tool_use IDs and their positions
        tool_use_ids = {}
        for i, message in enumerate(messages):
            if message.get('role') == 'assistant':
                content = message.get('content', [])
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'tool_use':
                            tool_use_ids[item.get('id')] = i
        
        # Check for missing tool_results after tool_use
        for tool_id, pos in tool_use_ids.items():
            # Check if there's a next message with tool_result
            if pos + 1 < len(messages):
                next_message = messages[pos + 1]
                if next_message.get('role') == 'user':
                    content = next_message.get('content', [])
                    if isinstance(content, list):
                        # Check if this tool_id has a matching tool_result
                        has_matching_result = False
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'tool_result' and item.get('tool_use_id') == tool_id:
                                has_matching_result = True
                                break
                        
                        # If no matching result, add a dummy tool_result
                        if not has_matching_result:
                            if isinstance(next_message['content'], list):
                                next_message['content'].append({
                                    'type': 'tool_result',
                                    'tool_use_id': tool_id,
                                    'content': {'result': 'No result available'}
                                })
                            else:
                                next_message['content'] = [{
                                    'type': 'tool_result',
                                    'tool_use_id': tool_id,
                                    'content': {'result': 'No result available'}
                                }]
            else:
                # No next message, add one with tool_result
                messages.append({
                    'role': 'user',
                    'content': [{
                        'type': 'tool_result',
                        'tool_use_id': tool_id,
                        'content': {'result': 'No result available'}
                    }]
                })
        
        # Filter out orphaned tool_results
        fixed_messages = []
        for message in messages:
            if message.get('role') == 'user':
                content = message.get('content', [])
                if isinstance(content, list):
                    fixed_content = []
                    has_orphaned_results = False
                    
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'tool_result':
                            if item.get('tool_use_id') in tool_use_ids:
                                fixed_content.append(item)
                            else:
                                has_orphaned_results = True
                        else:
                            fixed_content.append(item)
                    
                    if fixed_content or not has_orphaned_results:
                        fixed_message = message.copy()
                        fixed_message['content'] = fixed_content if fixed_content else "Continuing the conversation."
                        fixed_messages.append(fixed_message)
                    else:
                        # If all content was removed and there were orphaned results,
                        # add a simple continuation message
                        fixed_messages.append({
                            'role': 'user',
                            'content': 'Continuing the conversation.'
                        })
                else:
                    fixed_messages.append(message)
            else:
                fixed_messages.append(message)
        
        return fixed_messages
    
    def _execute_tool(self, tool_name: str, params: Dict) -> Dict:
        """Execute a tool and return the result"""
        # This should be overridden by subclasses to implement actual tool execution
        return {"error": f"Tool {tool_name} not implemented"}

class AviationToolHandler(ClaudeToolHandler):
    """Aviation-specific tool handler"""
    
    def _execute_tool(self, tool_name: str, params: Dict) -> Dict:
        """Execute aviation tools"""
        if tool_name == "get_flight_position":
            from aviation_data_access import aviation_data
            flight_id = params.get('flight_id')
            if flight_id:
                position = aviation_data.get_flight_position(flight_id)
                return {"position": position}
            return {"error": "Missing flight_id parameter"}
        
        elif tool_name == "search_aircraft":
            from aircraft_web_search import search_aircraft
            identifier = params.get('identifier')
            if identifier:
                results = search_aircraft(identifier)
                return results
            return {"error": "Missing identifier parameter"}
        
        return super()._execute_tool(tool_name, params)

# Example aviation tools definition
AVIATION_TOOLS = [
    {
        "name": "get_flight_position",
        "description": "Get the current position of an aircraft by registration number",
        "input_schema": {
            "type": "object",
            "properties": {
                "flight_id": {
                    "type": "string",
                    "description": "Aircraft registration number (e.g., N628TS)"
                }
            },
            "required": ["flight_id"]
        }
    },
    {
        "name": "search_aircraft",
        "description": "Search for aircraft information by registration or name",
        "input_schema": {
            "type": "object",
            "properties": {
                "identifier": {
                    "type": "string",
                    "description": "Aircraft registration or name (e.g., N628TS or ElonJet)"
                }
            },
            "required": ["identifier"]
        }
    }
]