"""
Crypto Performance Monitor - Track and optimize cryptocurrency assistant performance
"""

import time
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading
import boto3
from functools import wraps

class CryptoPerformanceMonitor:
    """Monitor and optimize cryptocurrency assistant performance"""
    
    def __init__(self):
        self.metrics = {
            "api_calls": 0,
            "api_errors": 0,
            "response_times": [],
            "cache_hits": 0,
            "cache_misses": 0,
            "queries_processed": 0,
            "prediction_queries": 0,
            "start_time": time.time()
        }
        
        self.cloudwatch = None
        try:
            self.cloudwatch = boto3.client('cloudwatch')
        except:
            print("CloudWatch client initialization failed - metrics will be stored locally only")
        
        # Start background thread for periodic reporting
        self.reporting_thread = threading.Thread(target=self._periodic_reporting, daemon=True)
        self.reporting_thread.start()
    
    def track_api_call(self, success: bool = True) -> None:
        """Track API call success/failure"""
        self.metrics["api_calls"] += 1
        if not success:
            self.metrics["api_errors"] += 1
    
    def track_response_time(self, response_time: float) -> None:
        """Track response time in seconds"""
        self.metrics["response_times"].append(response_time)
    
    def track_cache(self, hit: bool = True) -> None:
        """Track cache hit/miss"""
        if hit:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
    
    def track_query(self, query: str) -> None:
        """Track query processing"""
        self.metrics["queries_processed"] += 1
        
        # Track prediction queries
        if any(word in query.lower() for word in ['predict', 'forecast', 'potential', 'growth', 'future', '10x']):
            self.metrics["prediction_queries"] += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        uptime = time.time() - self.metrics["start_time"]
        
        # Calculate average response time
        avg_response_time = 0
        if self.metrics["response_times"]:
            avg_response_time = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
        
        # Calculate cache hit rate
        cache_total = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        cache_hit_rate = 0
        if cache_total > 0:
            cache_hit_rate = self.metrics["cache_hits"] / cache_total
        
        # Calculate error rate
        error_rate = 0
        if self.metrics["api_calls"] > 0:
            error_rate = self.metrics["api_errors"] / self.metrics["api_calls"]
        
        return {
            "uptime_seconds": uptime,
            "queries_processed": self.metrics["queries_processed"],
            "prediction_queries": self.metrics["prediction_queries"],
            "api_calls": self.metrics["api_calls"],
            "api_errors": self.metrics["api_errors"],
            "error_rate": error_rate,
            "avg_response_time": avg_response_time,
            "cache_hit_rate": cache_hit_rate,
            "timestamp": datetime.now().isoformat()
        }
    
    def _periodic_reporting(self) -> None:
        """Background thread for periodic metric reporting"""
        while True:
            try:
                # Sleep for 5 minutes
                time.sleep(300)
                
                # Get current stats
                stats = self.get_performance_stats()
                
                # Report to CloudWatch if available
                if self.cloudwatch:
                    try:
                        self.cloudwatch.put_metric_data(
                            Namespace='CryptoAssistant',
                            MetricData=[
                                {
                                    'MetricName': 'QueriesProcessed',
                                    'Value': self.metrics["queries_processed"],
                                    'Unit': 'Count'
                                },
                                {
                                    'MetricName': 'AvgResponseTime',
                                    'Value': stats["avg_response_time"],
                                    'Unit': 'Seconds'
                                },
                                {
                                    'MetricName': 'ErrorRate',
                                    'Value': stats["error_rate"] * 100,
                                    'Unit': 'Percent'
                                },
                                {
                                    'MetricName': 'CacheHitRate',
                                    'Value': stats["cache_hit_rate"] * 100,
                                    'Unit': 'Percent'
                                }
                            ]
                        )
                    except Exception as e:
                        print(f"CloudWatch metric reporting error: {str(e)}")
                
                # Reset certain metrics for the next period
                self.metrics["response_times"] = []
                
            except Exception as e:
                print(f"Performance monitoring error: {str(e)}")
    
    def optimize_query_processing(self, query: str) -> str:
        """
        Optimize query processing based on performance data
        
        Args:
            query: Original user query
            
        Returns:
            Optimized query with performance directives
        """
        # Get current performance stats
        stats = self.get_performance_stats()
        
        # If response times are high, add optimization directive
        if stats["avg_response_time"] > 2.0:  # More than 2 seconds
            query = f"[OPTIMIZE_SPEED] {query}"
        
        # If error rate is high, add reliability directive
        if stats["error_rate"] > 0.1:  # More than 10% errors
            query = f"[PREFER_CACHED_DATA] {query}"
        
        return query

def performance_tracking(func):
    """Decorator to track performance of a function"""
    @wraps(func)
    def wrapper(query: str, *args, **kwargs):
        # Get monitor instance
        monitor = crypto_performance_monitor
        
        # Track query
        monitor.track_query(query)
        
        # Optimize query if needed
        optimized_query = monitor.optimize_query_processing(query)
        
        # Measure response time
        start_time = time.time()
        
        try:
            # Call original function with optimized query
            result = func(optimized_query, *args, **kwargs)
            
            # Track successful API call
            monitor.track_api_call(True)
            
            return result
        except Exception as e:
            # Track failed API call
            monitor.track_api_call(False)
            raise e
        finally:
            # Track response time
            response_time = time.time() - start_time
            monitor.track_response_time(response_time)
    
    return wrapper

# Create singleton instance
crypto_performance_monitor = CryptoPerformanceMonitor()

# Test function
if __name__ == "__main__":
    # Simulate some activity
    monitor = crypto_performance_monitor
    
    # Simulate API calls
    for i in range(100):
        monitor.track_api_call(i % 10 != 0)  # 10% error rate
    
    # Simulate response times
    for i in range(50):
        monitor.track_response_time(0.5 + (i % 5) * 0.1)  # 0.5-0.9s
    
    # Simulate cache
    for i in range(80):
        monitor.track_cache(i % 4 != 0)  # 75% hit rate
    
    # Simulate queries
    monitor.track_query("What's the price of Bitcoin?")
    monitor.track_query("Predict Ethereum price next month")
    monitor.track_query("Which coins have 10x potential?")
    
    # Print stats
    print(json.dumps(monitor.get_performance_stats(), indent=2))