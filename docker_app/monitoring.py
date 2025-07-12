import time
import boto3
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-west-2')
        self.metrics = {}
    
    def track_response_time(self, assistant_type, duration):
        try:
            self.cloudwatch.put_metric_data(
                Namespace='ContinuumAssistant',
                MetricData=[{
                    'MetricName': 'ResponseTime',
                    'Dimensions': [{'Name': 'Assistant', 'Value': assistant_type}],
                    'Value': duration,
                    'Unit': 'Seconds',
                    'Timestamp': datetime.utcnow()
                }]
            )
        except:
            pass
    
    def track_error(self, assistant_type, error_type):
        try:
            self.cloudwatch.put_metric_data(
                Namespace='ContinuumAssistant',
                MetricData=[{
                    'MetricName': 'Errors',
                    'Dimensions': [
                        {'Name': 'Assistant', 'Value': assistant_type},
                        {'Name': 'ErrorType', 'Value': error_type}
                    ],
                    'Value': 1,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                }]
            )
        except:
            pass

monitor = PerformanceMonitor()

def time_assistant_call(assistant_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                monitor.track_response_time(assistant_type, duration)
                return result
            except Exception as e:
                duration = time.time() - start_time
                monitor.track_error(assistant_type, type(e).__name__)
                raise
        return wrapper
    return decorator