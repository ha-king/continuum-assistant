import streamlit as st
import json
import traceback
from datetime import datetime
import boto3
import pickle
import base64

class CrashPreventionSystem:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket_name = 'continuum-session-backup'
        
    def backup_session_state(self, user_id="anonymous"):
        """Backup critical session state to prevent data loss"""
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'tab_messages': st.session_state.get('tab_messages', {}),
                'tab_ids': st.session_state.get('tab_ids', [0]),
                'next_tab_id': st.session_state.get('next_tab_id', 1),
                'bp_data': st.session_state.get('bp_data', {}),
                'bp_stage': st.session_state.get('bp_stage', ''),
                'user_timezone': st.session_state.get('user_timezone', 'UTC'),
                'user_location': st.session_state.get('user_location', None),
                'intelligence_initialized': st.session_state.get('intelligence_initialized', False)
            }
            
            # Serialize and encode
            serialized = pickle.dumps(backup_data)
            encoded = base64.b64encode(serialized).decode()
            
            # Store in S3 with user-specific key
            key = f"session_backup/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.backup"
            
            try:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=encoded,
                    Metadata={'user_id': user_id, 'backup_type': 'session_state'}
                )
                return True
            except:
                # Fallback to local storage if S3 fails
                with open(f"/tmp/session_backup_{user_id}.json", 'w') as f:
                    json.dump(backup_data, f, default=str)
                return True
                
        except Exception as e:
            print(f"Backup failed: {str(e)}")
            return False
    
    def restore_session_state(self, user_id="anonymous"):
        """Restore session state from backup"""
        try:
            # Try S3 first
            try:
                response = self.s3.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=f"session_backup/{user_id}_"
                )
                
                if 'Contents' in response:
                    # Get most recent backup
                    latest_backup = max(response['Contents'], key=lambda x: x['LastModified'])
                    
                    obj = self.s3.get_object(Bucket=self.bucket_name, Key=latest_backup['Key'])
                    encoded_data = obj['Body'].read().decode()
                    serialized = base64.b64decode(encoded_data)
                    backup_data = pickle.loads(serialized)
                    
                    # Restore session state
                    for key, value in backup_data.items():
                        if key != 'timestamp' and key != 'user_id':
                            st.session_state[key] = value
                    
                    return True
            except:
                # Fallback to local storage
                try:
                    with open(f"/tmp/session_backup_{user_id}.json", 'r') as f:
                        backup_data = json.load(f)
                    
                    for key, value in backup_data.items():
                        if key != 'timestamp' and key != 'user_id':
                            st.session_state[key] = value
                    
                    return True
                except:
                    pass
            
            return False
            
        except Exception as e:
            print(f"Restore failed: {str(e)}")
            return False
    
    def detect_crash_conditions(self):
        """Detect conditions that might lead to crashes"""
        warnings = []
        
        # Check memory usage
        if len(st.session_state.get('tab_messages', {})) > 50:
            warnings.append("High memory usage: Many chat messages stored")
        
        # Check for large responses
        for tab_id, messages in st.session_state.get('tab_messages', {}).items():
            for msg in messages[-5:]:  # Check last 5 messages
                if len(msg.get('content', '')) > 10000:
                    warnings.append(f"Large response detected in tab {tab_id}")
        
        # Check for stuck processes
        if st.session_state.get('bp_stage') and not st.session_state.get('bp_data'):
            warnings.append("Business plan process may be stuck")
        
        return warnings
    
    def safe_execute(self, func, *args, **kwargs):
        """Execute function with error handling and recovery"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_info = {
                'function': func.__name__ if hasattr(func, '__name__') else str(func),
                'error': str(e),
                'traceback': traceback.format_exc(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Log error
            print(f"Safe execution failed: {error_info}")
            
            # Try to backup current state before potential crash
            self.backup_session_state()
            
            # Return safe fallback
            return f"Error in {error_info['function']}: {str(e)}"
    
    def cleanup_session_state(self):
        """Clean up session state to prevent memory issues"""
        try:
            # Limit chat history per tab
            if 'tab_messages' in st.session_state:
                for tab_id in st.session_state.tab_messages:
                    messages = st.session_state.tab_messages[tab_id]
                    if len(messages) > 100:  # Keep last 100 messages
                        st.session_state.tab_messages[tab_id] = messages[-100:]
            
            # Clean up old business plan data
            if st.session_state.get('bp_stage') == 'complete' and 'generated_bp' in st.session_state:
                # Keep only essential data after generation
                if len(st.session_state.get('generated_bp', '')) > 50000:
                    st.session_state.generated_bp = st.session_state.generated_bp[:50000] + "...[truncated]"
            
            return True
            
        except Exception as e:
            print(f"Cleanup failed: {str(e)}")
            return False
    
    def create_crash_recovery_interface(self):
        """Create UI for crash recovery (simplified to avoid component issues)"""
        # Simplified interface without problematic components
        warnings = self.detect_crash_conditions()
        if len(warnings) > 3:
            # Auto-cleanup if too many warnings
            self.cleanup_session_state()
    
    def monitor_system_health(self):
        """Monitor system health and provide status"""
        health_status = {
            'session_size': len(str(st.session_state)),
            'active_tabs': len(st.session_state.get('tab_ids', [])),
            'total_messages': sum(len(msgs) for msgs in st.session_state.get('tab_messages', {}).values()),
            'warnings': len(self.detect_crash_conditions())
        }
        
        return health_status

# Global instance
crash_prevention = CrashPreventionSystem()

def initialize_crash_prevention():
    """Initialize crash prevention system (simplified)"""
    # Auto-backup every 20 interactions (reduced frequency)
    total_messages = sum(len(msgs) for msgs in st.session_state.get('tab_messages', {}).values())
    if total_messages > 0 and total_messages % 20 == 0:
        try:
            user_id = st.session_state.get('user_id', 'anonymous')
            crash_prevention.backup_session_state(user_id)
        except:
            pass
    
    # Simplified recovery interface
    crash_prevention.create_crash_recovery_interface()
    
    # Auto-cleanup if needed
    if total_messages > 150:
        crash_prevention.cleanup_session_state()

def safe_execute_function(func, *args, **kwargs):
    """Safely execute any function with crash prevention"""
    return crash_prevention.safe_execute(func, *args, **kwargs)

def get_system_health():
    """Get system health status"""
    return crash_prevention.monitor_system_health()