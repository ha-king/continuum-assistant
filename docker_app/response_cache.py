import time
import hashlib
import json
import os
import boto3

class ResponseCache:
    def __init__(self, ttl=300):  # 5 minutes TTL by default
        self.local_cache = {}
        self.timestamps = {}
        self.ttl = ttl
        self.region = os.environ.get("AWS_REGION", "us-west-2")
        self.table_name = os.environ.get("RESPONSE_CACHE_TABLE", "response-cache")
        
        # Initialize DynamoDB client if in production
        if not os.environ.get("LOCAL_DEV"):
            try:
                self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
                self.table = self.dynamodb.Table(self.table_name)
                self.enabled = True
            except Exception as e:
                print(f"Failed to initialize DynamoDB for response cache: {str(e)}")
                self.enabled = False
        else:
            self.enabled = False
    
    def get_cache_key(self, query, model=None, user_id=None):
        """Generate a cache key from query and optional parameters"""
        # Normalize inputs
        query = query.strip().lower()
        components = [query]
        
        if model:
            components.append(str(model))
        
        if user_id and user_id != 'anonymous':
            components.append(user_id)
        
        # Create hash
        key_string = ":".join(components)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key):
        """Get response from cache"""
        # Check local cache first
        current_time = time.time()
        if key in self.local_cache and current_time - self.timestamps.get(key, 0) < self.ttl:
            print(f"Cache hit (local): {key[:8]}...")
            return self.local_cache[key]
        
        # If not in local cache, try DynamoDB
        if self.enabled:
            try:
                response = self.table.get_item(Key={'cache_key': key})
                if 'Item' in response:
                    item = response['Item']
                    timestamp = item.get('timestamp', 0)
                    
                    # Check if item is still valid
                    if current_time - timestamp < self.ttl:
                        # Update local cache
                        self.local_cache[key] = item['response']
                        self.timestamps[key] = timestamp
                        print(f"Cache hit (DynamoDB): {key[:8]}...")
                        return item['response']
            except Exception as e:
                print(f"Error retrieving from cache: {str(e)}")
        
        return None
    
    def set(self, key, response):
        """Store response in cache"""
        current_time = time.time()
        
        # Update local cache
        self.local_cache[key] = response
        self.timestamps[key] = current_time
        
        # Update DynamoDB if enabled
        if self.enabled:
            try:
                self.table.put_item(
                    Item={
                        'cache_key': key,
                        'response': response,
                        'timestamp': current_time,
                        'ttl': int(current_time + self.ttl * 2)  # TTL for DynamoDB auto-deletion
                    }
                )
            except Exception as e:
                print(f"Error storing in cache: {str(e)}")
        
        # Clean up local cache periodically
        if len(self.local_cache) > 1000:
            self._cleanup_local_cache()
    
    def _cleanup_local_cache(self):
        """Remove expired items from local cache"""
        current_time = time.time()
        expired_keys = [k for k, v in self.timestamps.items() if current_time - v > self.ttl]
        
        for key in expired_keys:
            if key in self.local_cache:
                del self.local_cache[key]
            if key in self.timestamps:
                del self.timestamps[key]
        
        print(f"Cache cleanup: removed {len(expired_keys)} expired entries, {len(self.local_cache)} remaining")

# Global instance
response_cache = ResponseCache()