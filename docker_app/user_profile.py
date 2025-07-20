import json
import boto3
import re
from datetime import datetime
import os

class UserProfileManager:
    def __init__(self):
        self.profiles = {}
        self.region = os.environ.get("AWS_REGION", "us-west-2")
        self.table_name = os.environ.get("USER_PROFILES_TABLE", "user-profiles")
        
        # Initialize DynamoDB client if in production
        if not os.environ.get("LOCAL_DEV"):
            try:
                self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
                self.table = self.dynamodb.Table(self.table_name)
                self.enabled = True
            except Exception as e:
                print(f"Failed to initialize DynamoDB for user profiles: {str(e)}")
                self.enabled = False
        else:
            self.enabled = False
    
    def extract_personal_info(self, message):
        """Extract personal information from user messages"""
        personal_info = {}
        
        # Extract name patterns
        name_patterns = [
            r"(?:my name is|I am|I'm|call me) ([A-Z][a-z]+(?: [A-Z][a-z]+)*)",
            r"([A-Z][a-z]+(?: [A-Z][a-z]+)*) (?:here|speaking)"
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, message)
            if matches:
                personal_info['name'] = matches[0]
                break
        
        # Extract location patterns
        location_patterns = [
            r"(?:I live in|I'm from|I am from|I'm in) ([A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)",
            r"(?:based in|located in) ([A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)"
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, message)
            if matches:
                personal_info['location'] = matches[0]
                break
        
        # Extract profession/role
        profession_patterns = [
            r"(?:I am a|I'm a|I work as a|I'm working as a) ([A-Za-z\s]+)",
            r"(?:my job is|my profession is|my role is) ([A-Za-z\s]+)"
        ]
        
        for pattern in profession_patterns:
            matches = re.findall(pattern, message)
            if matches:
                personal_info['profession'] = matches[0]
                break
        
        # Extract preferences
        if "prefer" in message.lower():
            preference_patterns = [
                r"(?:I prefer|I like) ([A-Za-z\s]+)",
                r"(?:my preference is) ([A-Za-z\s]+)"
            ]
            
            for pattern in preference_patterns:
                matches = re.findall(pattern, message.lower())
                if matches:
                    personal_info['preference'] = matches[0]
                    break
        
        return personal_info
    
    def update_user_profile(self, user_id, message):
        """Update user profile with extracted information"""
        if not user_id or user_id == 'anonymous':
            return {}
        
        # Extract personal information from message
        extracted_info = self.extract_personal_info(message)
        if not extracted_info:
            return {}
        
        # Get existing profile or create new one
        profile = self.get_user_profile(user_id)
        if not profile:
            profile = {
                'user_id': user_id,
                'created_at': datetime.now().isoformat(),
                'personal_info': {}
            }
        
        # Update profile with new information
        for key, value in extracted_info.items():
            profile['personal_info'][key] = value
        
        profile['updated_at'] = datetime.now().isoformat()
        
        # Save updated profile
        self.profiles[user_id] = profile
        self._save_profile_to_db(user_id, profile)
        
        return extracted_info
    
    def get_user_profile(self, user_id):
        """Get user profile from cache or database"""
        if not user_id or user_id == 'anonymous':
            return {}
        
        # Check cache first
        if user_id in self.profiles:
            return self.profiles[user_id]
        
        # Try to load from database
        profile = self._load_profile_from_db(user_id)
        if profile:
            self.profiles[user_id] = profile
            return profile
        
        return {}
    
    def get_personal_context(self, user_id):
        """Get personal context string for use in prompts"""
        profile = self.get_user_profile(user_id)
        if not profile or 'personal_info' not in profile:
            return ""
        
        personal_info = profile.get('personal_info', {})
        context_parts = []
        
        if 'name' in personal_info:
            context_parts.append(f"User's name: {personal_info['name']}")
        
        if 'location' in personal_info:
            context_parts.append(f"User's location: {personal_info['location']}")
        
        if 'profession' in personal_info:
            context_parts.append(f"User's profession: {personal_info['profession']}")
        
        if 'preference' in personal_info:
            context_parts.append(f"User's preference: {personal_info['preference']}")
        
        if context_parts:
            return "User Personal Context: " + "; ".join(context_parts)
        
        return ""
    
    def _save_profile_to_db(self, user_id, profile):
        """Save profile to DynamoDB"""
        if not self.enabled:
            return
        
        try:
            self.table.put_item(Item=profile)
        except Exception as e:
            print(f"Failed to save user profile to DynamoDB: {str(e)}")
    
    def _load_profile_from_db(self, user_id):
        """Load profile from DynamoDB"""
        if not self.enabled:
            return {}
        
        try:
            response = self.table.get_item(Key={'user_id': user_id})
            return response.get('Item', {})
        except Exception as e:
            print(f"Failed to load user profile from DynamoDB: {str(e)}")
            return {}

# Global instance
user_profile_manager = UserProfileManager()

def update_user_profile(user_id, message):
    """Update user profile with information from message"""
    return user_profile_manager.update_user_profile(user_id, message)

def get_personal_context(user_id):
    """Get personal context for user"""
    return user_profile_manager.get_personal_context(user_id)

def get_user_profile(user_id):
    """Get complete user profile"""
    return user_profile_manager.get_user_profile(user_id)