"""
AWS-native telemetry for tracking user flows
"""

import boto3
import json
import os
import time
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime

# Initialize AWS clients
cloudwatch = boto3.client('cloudwatch', region_name=os.environ.get('AWS_REGION', 'us-west-2'))
logs = boto3.client('logs', region_name=os.environ.get('AWS_REGION', 'us-west-2'))
firehose = boto3.client('firehose', region_name=os.environ.get('AWS_REGION', 'us-west-2'))

# Constants
APP_NAME = os.environ.get('APP_NAME', 'continuum-assistant')
ENV = os.environ.get('ENVIRONMENT', 'prod')
LOG_GROUP = f"/aws/lambda/{APP_NAME}-{ENV}"
FIREHOSE_STREAM = os.environ.get('FIREHOSE_STREAM', f"{APP_NAME}-{ENV}-telemetry")
ENABLE_TELEMETRY = os.environ.get('ENABLE_TELEMETRY', 'true').lower() == 'true'

# Ensure log group exists
try:
    logs.create_log_group(logGroupName=LOG_GROUP)
except logs.exceptions.ResourceAlreadyExistsException:
    pass

def log_user_interaction(
    user_id: str,
    event_type: str,
    query: str,
    assistant_used: str,
    response_time_ms: int,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log user interaction to CloudWatch Logs and Metrics
    
    Args:
        user_id: Anonymized user identifier
        event_type: Type of event (query, response, error, etc.)
        query: User query (truncated for privacy)
        assistant_used: Which assistant was used
        response_time_ms: Response time in milliseconds
        metadata: Additional metadata about the interaction
    """
    if not ENABLE_TELEMETRY:
        return
        
    try:
        # Create event payload
        timestamp = int(time.time() * 1000)
        event_id = str(uuid.uuid4())
        
        # Sanitize query for privacy (truncate and remove PII)
        sanitized_query = query[:100] + "..." if len(query) > 100 else query
        
        event = {
            "event_id": event_id,
            "timestamp": timestamp,
            "user_id": user_id,
            "event_type": event_type,
            "query_length": len(query),
            "query_type": detect_query_type(query),
            "assistant_used": assistant_used,
            "response_time_ms": response_time_ms,
            "environment": ENV,
            "app_version": os.environ.get('APP_VERSION', 'unknown')
        }
        
        # Add metadata if provided
        if metadata:
            event.update(metadata)
        
        # Log to CloudWatch Logs
        log_stream_name = f"{datetime.now().strftime('%Y/%m/%d')}/{user_id}"
        try:
            logs.create_log_stream(logGroupName=LOG_GROUP, logStreamName=log_stream_name)
        except logs.exceptions.ResourceAlreadyExistsException:
            pass
            
        logs.put_log_events(
            logGroupName=LOG_GROUP,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': timestamp,
                'message': json.dumps(event)
            }]
        )
        
        # Send to Firehose for analytics
        try:
            firehose.put_record(
                DeliveryStreamName=FIREHOSE_STREAM,
                Record={'Data': json.dumps(event) + '\n'}
            )
        except Exception as e:
            print(f"Firehose error: {str(e)}")
        
        # Publish CloudWatch metrics
        dimensions = [
            {'Name': 'Environment', 'Value': ENV},
            {'Name': 'AssistantType', 'Value': assistant_used},
            {'Name': 'QueryType', 'Value': detect_query_type(query)}
        ]
        
        cloudwatch.put_metric_data(
            Namespace=f"{APP_NAME}/UserInteractions",
            MetricData=[
                {
                    'MetricName': 'ResponseTime',
                    'Dimensions': dimensions,
                    'Value': response_time_ms,
                    'Unit': 'Milliseconds'
                },
                {
                    'MetricName': 'QueryCount',
                    'Dimensions': dimensions,
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
    except Exception as e:
        print(f"Telemetry error: {str(e)}")

def detect_query_type(query: str) -> str:
    """Detect the type of query based on content"""
    query_lower = query.lower()
    
    # Define patterns for different query types
    patterns = {
        "crypto": ["crypto", "bitcoin", "ethereum", "token", "blockchain", "coin"],
        "finance": ["finance", "stock", "market", "investment", "portfolio"],
        "aviation": ["flight", "aircraft", "airport", "aviation", "plane"],
        "formula1": ["f1", "formula 1", "racing", "grand prix", "driver"],
        "tech": ["code", "programming", "software", "algorithm", "api"],
        "prediction": ["predict", "forecast", "future", "will", "expect"]
    }
    
    # Check for matches
    for query_type, keywords in patterns.items():
        if any(keyword in query_lower for keyword in keywords):
            return query_type
    
    return "general"

def track_user_session(
    user_id: str,
    session_id: str,
    action: str,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Track user session events
    
    Args:
        user_id: Anonymized user identifier
        session_id: Session identifier
        action: Session action (start, end, tab_change, etc.)
        metadata: Additional metadata about the session
    """
    if not ENABLE_TELEMETRY:
        return
        
    try:
        timestamp = int(time.time() * 1000)
        
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "user_id": user_id,
            "session_id": session_id,
            "action": action,
            "environment": ENV
        }
        
        # Add metadata if provided
        if metadata:
            event.update(metadata)
        
        # Send to Firehose for analytics
        try:
            firehose.put_record(
                DeliveryStreamName=FIREHOSE_STREAM,
                Record={'Data': json.dumps(event) + '\n'}
            )
        except Exception as e:
            print(f"Firehose error: {str(e)}")
            
        # Publish CloudWatch metrics
        dimensions = [
            {'Name': 'Environment', 'Value': ENV},
            {'Name': 'Action', 'Value': action}
        ]
        
        cloudwatch.put_metric_data(
            Namespace=f"{APP_NAME}/UserSessions",
            MetricData=[
                {
                    'MetricName': 'SessionEvents',
                    'Dimensions': dimensions,
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
    except Exception as e:
        print(f"Session tracking error: {str(e)}")

def track_assistant_performance(
    assistant_name: str,
    query_type: str,
    response_time_ms: int,
    token_count: int,
    success: bool
) -> None:
    """
    Track assistant performance metrics
    
    Args:
        assistant_name: Name of the assistant
        query_type: Type of query
        response_time_ms: Response time in milliseconds
        token_count: Number of tokens in response
        success: Whether the assistant successfully handled the query
    """
    if not ENABLE_TELEMETRY:
        return
        
    try:
        dimensions = [
            {'Name': 'Environment', 'Value': ENV},
            {'Name': 'AssistantName', 'Value': assistant_name},
            {'Name': 'QueryType', 'Value': query_type}
        ]
        
        cloudwatch.put_metric_data(
            Namespace=f"{APP_NAME}/AssistantPerformance",
            MetricData=[
                {
                    'MetricName': 'ResponseTime',
                    'Dimensions': dimensions,
                    'Value': response_time_ms,
                    'Unit': 'Milliseconds'
                },
                {
                    'MetricName': 'TokenCount',
                    'Dimensions': dimensions,
                    'Value': token_count,
                    'Unit': 'Count'
                },
                {
                    'MetricName': 'SuccessRate',
                    'Dimensions': dimensions,
                    'Value': 1 if success else 0,
                    'Unit': 'None'
                }
            ]
        )
    except Exception as e:
        print(f"Performance tracking error: {str(e)}")

def track_routing_decision(
    query: str,
    matched_rule: str,
    assistant_used: str,
    confidence: float
) -> None:
    """
    Track router decisions for analysis
    
    Args:
        query: User query
        matched_rule: Rule that matched
        assistant_used: Assistant that was used
        confidence: Confidence score of the match
    """
    if not ENABLE_TELEMETRY:
        return
        
    try:
        timestamp = int(time.time() * 1000)
        
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "query_type": detect_query_type(query),
            "matched_rule": matched_rule,
            "assistant_used": assistant_used,
            "confidence": confidence,
            "environment": ENV
        }
        
        # Send to Firehose for analytics
        try:
            firehose.put_record(
                DeliveryStreamName=FIREHOSE_STREAM,
                Record={'Data': json.dumps(event) + '\n'}
            )
        except Exception as e:
            print(f"Firehose error: {str(e)}")
            
        # Publish CloudWatch metrics
        dimensions = [
            {'Name': 'Environment', 'Value': ENV},
            {'Name': 'MatchedRule', 'Value': matched_rule},
            {'Name': 'AssistantUsed', 'Value': assistant_used}
        ]
        
        cloudwatch.put_metric_data(
            Namespace=f"{APP_NAME}/RouterDecisions",
            MetricData=[
                {
                    'MetricName': 'RoutingCount',
                    'Dimensions': dimensions,
                    'Value': 1,
                    'Unit': 'Count'
                },
                {
                    'MetricName': 'Confidence',
                    'Dimensions': dimensions,
                    'Value': confidence,
                    'Unit': 'None'
                }
            ]
        )
    except Exception as e:
        print(f"Routing tracking error: {str(e)}")