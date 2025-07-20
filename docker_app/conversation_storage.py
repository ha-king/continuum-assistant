"""
Conversation Storage - Persistent storage for user conversation history using baggage-claim pattern
"""

import boto3
import json
import time
import os
from datetime import datetime
import streamlit as st

class ConversationStorage:
    """Handles persistent storage of conversation history using S3 for data and DynamoDB for metadata"""
    
    def __init__(self):
        """Initialize the conversation storage with DynamoDB and S3 connections"""
        self.table_name = os.environ.get("CONVERSATION_TABLE", "user-conversations")
        self.bucket_name = os.environ.get("CONVERSATION_BUCKET", "user-conversations-data")
        self.region = os.environ.get("AWS_REGION", "us-east-1")
        
        try:
            # Initialize AWS clients
            self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
            self.s3 = boto3.client('s3', region_name=self.region)
            self.table = self.dynamodb.Table(self.table_name)
            self.enabled = True
        except Exception as e:
            print(f"Failed to initialize AWS clients: {str(e)}")
            self.enabled = False
    
    def save_conversation(self, user_id, messages):
        """Save conversation history using baggage-claim pattern"""
        if not self.enabled or not user_id or user_id == 'anonymous':
            return False
        
        try:
            # Create a conversation record
            timestamp = int(time.time())
            
            # Generate S3 key for this conversation
            s3_key = f"conversations/{user_id}/{timestamp}.json"
            
            # Store full conversation data in S3
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json.dumps(messages),
                ContentType='application/json'
            )
            
            # Store metadata and reference in DynamoDB
            self.table.put_item(
                Item={
                    'conversation_id': user_id,
                    'user_id': user_id,
                    'last_updated': timestamp,
                    'message_count': len(messages),
                    's3_key': s3_key,
                    'last_message': messages[-1]['content'][:100] if messages else ""  # Preview of last message
                }
            )
            return True
        except Exception as e:
            print(f"Failed to save conversation: {str(e)}")
            return False
    
    def load_conversation(self, user_id):
        """Load conversation history using baggage-claim pattern"""
        if not self.enabled or not user_id or user_id == 'anonymous':
            return []
        
        try:
            # Get metadata from DynamoDB
            response = self.table.get_item(
                Key={
                    'conversation_id': user_id
                }
            )
            
            if 'Item' not in response:
                return []
            
            # Get S3 key from metadata
            s3_key = response['Item'].get('s3_key')
            if not s3_key:
                return []
            
            # Retrieve full conversation from S3
            s3_response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            # Parse and return the conversation data
            conversation_data = json.loads(s3_response['Body'].read().decode('utf-8'))
            return conversation_data
        except Exception as e:
            print(f"Failed to load conversation: {str(e)}")
            return []
    
    def delete_conversation(self, user_id):
        """Delete conversation history"""
        if not self.enabled or not user_id or user_id == 'anonymous':
            return False
        
        try:
            # Get metadata from DynamoDB
            response = self.table.get_item(
                Key={
                    'conversation_id': user_id
                }
            )
            
            if 'Item' in response and 's3_key' in response['Item']:
                # Delete S3 object
                self.s3.delete_object(
                    Bucket=self.bucket_name,
                    Key=response['Item']['s3_key']
                )
            
            # Delete DynamoDB item
            self.table.delete_item(
                Key={
                    'conversation_id': user_id
                }
            )
            return True
        except Exception as e:
            print(f"Failed to delete conversation: {str(e)}")
            return False

# Global instance
conversation_storage = ConversationStorage()

def load_user_conversation(user_id):
    """Load conversation for a user and initialize session state"""
    if not user_id or user_id == 'anonymous':
        return
    
    # Initialize messages if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Load conversation history
    messages = conversation_storage.load_conversation(user_id)
    if messages:
        st.session_state.messages = messages

def save_user_conversation(user_id):
    """Save conversation history"""
    if not user_id or user_id == 'anonymous':
        return
    
    if "messages" in st.session_state:
        messages = st.session_state.messages
        conversation_storage.save_conversation(user_id, messages)