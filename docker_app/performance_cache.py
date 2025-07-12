import json
import hashlib
from datetime import datetime, timedelta

class SimpleCache:
    def __init__(self, ttl_minutes=5):
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return data
            del self.cache[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = (value, datetime.now())
    
    def clear_expired(self):
        now = datetime.now()
        expired = [k for k, (_, ts) in self.cache.items() if now - ts >= self.ttl]
        for k in expired:
            del self.cache[k]

# Global cache instance
response_cache = SimpleCache(ttl_minutes=3)

def cache_key(query, assistant_type):
    return hashlib.md5(f"{assistant_type}:{query}".encode()).hexdigest()[:16]

def get_cached_response(query, assistant_type):
    key = cache_key(query, assistant_type)
    return response_cache.get(key)

def cache_response(query, assistant_type, response):
    key = cache_key(query, assistant_type)
    response_cache.set(key, response)