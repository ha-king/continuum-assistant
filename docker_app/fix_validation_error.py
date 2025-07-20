#!/usr/bin/env python3
\"\"\"
Fix for Claude API ValidationException:
'The number of toolResult blocks at messages.30.content exceeds the number of toolUse blocks of previous turn'
\"\"\"

import boto3
import json
from typing import List, Dict, Any

def fix_conversation_history(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Fix the conversation history by ensuring tool_use and tool_result blocks are properly matched
    
    Args:
        messages: The conversation history with potential mismatches
        
    Returns:
        Fixed conversation history with properly matched tool_use and tool_result blocks
    """
    fixed_messages = []
    tool_use_ids = set()
    tool_result_ids = set()
    
    # First pass: collect all tool_use IDs
    for i, message in enumerate(messages):
        if message.get('role') == 'assistant':
            content = message.get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        tool_use_ids.add(item.get('id'))
    
    # Second pass: collect all tool_result IDs
    for i, message in enumerate(messages):
        if message.get('role') == 'user':
            content = message.get('content', [])
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_result':
                        tool_result_ids.add(item.get('tool_use_id'))
    
    # Find orphaned tool_result IDs (results without matching tool_use)
    orphaned_results = tool_result_ids - tool_use_ids
    
    # Third pass: build fixed conversation by removing orphaned tool_results
    for i, message in enumerate(messages):
        if message.get('role') == 'user':
            content = message.get('content', [])
            if isinstance(content, list):
                fixed_content = []
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_result':
                        if item.get('tool_use_id') not in orphaned_results:
                            fixed_content.append(item)
                    else:
                        fixed_content.append(item)
                
                if fixed_content:  # Only add if there's content left
                    fixed_message = message.copy()
                    fixed_message['content'] = fixed_content
                    fixed_messages.append(fixed_message)
                else:
                    # If all content was removed, convert to a simple text message
                    fixed_messages.append({
                        'role': 'user',
                        'content': 'Continuing the conversation.'
                    })
            else:
                fixed_messages.append(message)
        else:
            fixed_messages.append(message)
    
    return fixed_messages

def apply_fix_to_conversation(conversation_id: str = None):
    """
    Apply the fix to a specific conversation or the current conversation
    
    Args:
        conversation_id: Optional ID of the conversation to fix
    """
    try:
        # In a real implementation, you would load the conversation from a database
        # For this example, we'll simulate loading from a file
        
        # Load conversation history
        try:
            with open(f"conversation_{conversation_id or 'current'}.json", "r") as f:
                messages = json.load(f)
        except FileNotFoundError:
            print(f"Conversation file not found. Creating a new one.")
            messages = []
        
        # Fix the conversation history
        fixed_messages = fix_conversation_history(messages)
        
        # Save the fixed conversation
        with open(f"conversation_{conversation_id or 'current'}_fixed.json", "w") as f:
            json.dump(fixed_messages, f, indent=2)
        
        print(f"Fixed conversation saved to conversation_{conversation_id or 'current'}_fixed.json")
        print(f"Original message count: {len(messages)}")
        print(f"Fixed message count: {len(fixed_messages)}")
        
        return fixed_messages
    except Exception as e:
        print(f"Error fixing conversation: {str(e)}")
        return None

def fix_claude_conversation(bedrock_client, model_id, messages):
    """
    Fix and retry a Claude conversation that failed with ValidationException
    
    Args:
        bedrock_client: Boto3 bedrock-runtime client
        model_id: Claude model ID
        messages: The conversation history that caused the error
        
    Returns:
        The response from Claude after fixing the conversation
    """
    # Fix the conversation history
    fixed_messages = fix_conversation_history(messages)
    
    # Retry the conversation with fixed messages
    try:
        response = bedrock_client.converse(
            modelId=model_id,
            messages=fixed_messages
        )
        return response
    except Exception as e:
        print(f"Error after fixing conversation: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    apply_fix_to_conversation()