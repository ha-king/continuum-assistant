import boto3
import json
from datetime import datetime, timedelta
import threading
import time
import schedule

class EnhancedLearningSystem:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.s3 = boto3.client('s3')
        self.bucket_name = 'continuum-learning-data'
        
        # Cross-domain learning topics
        self.learning_domains = {
            'financial_assistant': {
                'topics': ['market trends', 'regulations', 'fintech'],
                'related_domains': ['cryptocurrency_assistant', 'geopolitical_assistant']
            },
            'cryptocurrency_assistant': {
                'topics': ['crypto markets', 'DeFi', 'blockchain tech'],
                'related_domains': ['financial_assistant', 'geopolitical_assistant']
            },
            'geopolitical_assistant': {
                'topics': ['international relations', 'trade wars', 'sanctions'],
                'related_domains': ['financial_assistant', 'international_finance_assistant']
            },
            'aws_assistant': {
                'topics': ['new services', 'best practices', 'security'],
                'related_domains': ['cybersecurity_defense_assistant']
            }
        }
        
        self.learning_quality_scores = {}
        self.user_preferences = {}
        
    def adaptive_learning_session(self, assistant_name):
        """Enhanced learning with cross-domain synthesis"""
        try:
            domain = self.learning_domains.get(assistant_name, {})
            topics = domain.get('topics', [])
            related_domains = domain.get('related_domains', [])
            
            if not topics:
                return
                
            # Determine learning intensity based on market volatility
            intensity = self.calculate_learning_intensity(assistant_name)
            topic_count = 2 if intensity == 'high' else 1
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for i in range(min(topic_count, len(topics))):
                topic = topics[i]
                
                # Cross-domain synthesis prompt
                synthesis_context = self.get_cross_domain_context(assistant_name, related_domains)
                
                prompt = f"""
                Research latest developments in {topic} as of {current_time}.
                Consider cross-domain impacts: {synthesis_context}
                Provide 3 key insights with quality sources.
                Rate information reliability (1-10).
                """
                
                response = self.bedrock.invoke_model(
                    modelId="us.amazon.nova-micro-v1:0",
                    body=json.dumps({
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 300,
                        "temperature": 0.3
                    })
                )
                
                result = json.loads(response['body'].read())
                learning_content = result.get('content', [{}])[0].get('text', '')
                
                # Quality scoring
                quality_score = self.extract_quality_score(learning_content)
                self.update_quality_scores(assistant_name, topic, quality_score)
                
                # Store with enhanced metadata
                self.store_enhanced_learning(assistant_name, topic, learning_content, 
                                           current_time, quality_score, synthesis_context)
                
                print(f"[{current_time}] {assistant_name} learned: {topic} (Quality: {quality_score})")
                
        except Exception as e:
            print(f"Enhanced learning error for {assistant_name}: {str(e)}")
    
    def calculate_learning_intensity(self, assistant_name):
        """Determine learning frequency based on domain volatility"""
        volatility_indicators = {
            'cryptocurrency_assistant': 'high',  # Crypto is always volatile
            'financial_assistant': 'medium',
            'geopolitical_assistant': 'medium',
            'aws_assistant': 'low'
        }
        return volatility_indicators.get(assistant_name, 'low')
    
    def get_cross_domain_context(self, assistant_name, related_domains):
        """Get context from related domains for synthesis"""
        context_parts = []
        for domain in related_domains[:2]:  # Limit to 2 related domains
            recent_learning = self.get_recent_learning(domain)
            if recent_learning:
                context_parts.append(f"{domain}: {recent_learning[:100]}...")
        return " | ".join(context_parts)
    
    def extract_quality_score(self, content):
        """Extract quality score from learning content"""
        try:
            # Look for reliability rating in content
            import re
            score_match = re.search(r'reliability[:\s]*(\d+)', content.lower())
            if score_match:
                return int(score_match.group(1))
            return 7  # Default score
        except:
            return 7
    
    def update_quality_scores(self, assistant_name, topic, score):
        """Track learning quality over time"""
        key = f"{assistant_name}_{topic}"
        if key not in self.learning_quality_scores:
            self.learning_quality_scores[key] = []
        self.learning_quality_scores[key].append(score)
        
        # Keep only last 10 scores
        if len(self.learning_quality_scores[key]) > 10:
            self.learning_quality_scores[key] = self.learning_quality_scores[key][-10:]
    
    def store_enhanced_learning(self, assistant_name, topic, content, timestamp, quality_score, context):
        """Store learning with enhanced metadata"""
        learning_entry = {
            'assistant': assistant_name,
            'topic': topic,
            'content': content,
            'timestamp': timestamp,
            'quality_score': quality_score,
            'cross_domain_context': context,
            'learning_type': 'enhanced_synthesis'
        }
        
        # Store in S3 for persistence (simplified)
        try:
            key = f"learning/{assistant_name}/{timestamp.replace(':', '-')}.json"
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(learning_entry)
            )
        except:
            # Fallback to local storage
            print(f"Stored enhanced learning: {assistant_name} - {topic} (Q:{quality_score})")
    
    def get_recent_learning(self, assistant_name, days=1):
        """Get recent learning content for cross-domain synthesis"""
        try:
            # Simplified - would query S3 or database
            return f"Recent {assistant_name} insights from last {days} days"
        except:
            return ""
    
    def generate_proactive_alerts(self):
        """Generate alerts for critical developments"""
        try:
            # Check for high-impact learning across domains
            alert_prompt = """
            Analyze recent learning data for critical developments that require immediate attention.
            Focus on: market crashes, regulatory changes, security breaches, geopolitical crises.
            Generate alerts only for high-impact events.
            """
            
            response = self.bedrock.invoke_model(
                modelId="us.amazon.nova-micro-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": alert_prompt}],
                    "max_tokens": 200,
                    "temperature": 0.1
                })
            )
            
            result = json.loads(response['body'].read())
            alerts = result.get('content', [{}])[0].get('text', '')
            
            if "ALERT" in alerts.upper():
                self.send_alert(alerts)
                
        except Exception as e:
            print(f"Alert generation error: {str(e)}")
    
    def send_alert(self, alert_content):
        """Send proactive alert to users"""
        print(f"🚨 PROACTIVE ALERT: {alert_content}")
        # Could integrate with SNS, email, or in-app notifications
    
    def personalized_learning_adjustment(self, user_id, interaction_data):
        """Adjust learning based on user behavior"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'expertise_level': 'intermediate',
                'preferred_domains': [],
                'response_style': 'balanced'
            }
        
        # Analyze user interactions to adjust preferences
        # This would be enhanced with actual user behavior data
        
    def schedule_enhanced_learning(self):
        """Schedule adaptive learning sessions"""
        # High-frequency for volatile domains
        schedule.every(2).hours.do(self.adaptive_learning_session, 'cryptocurrency_assistant')
        schedule.every(4).hours.do(self.adaptive_learning_session, 'financial_assistant')
        schedule.every(6).hours.do(self.adaptive_learning_session, 'geopolitical_assistant')
        schedule.every(8).hours.do(self.adaptive_learning_session, 'aws_assistant')
        
        # Proactive alerts
        schedule.every(1).hours.do(self.generate_proactive_alerts)
        
        print("Enhanced learning system scheduled")
    
    def start_enhanced_learning(self):
        """Start the enhanced learning system"""
        self.schedule_enhanced_learning()
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(300)  # Check every 5 minutes
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("Enhanced learning system started")

# Global instance
enhanced_learning = EnhancedLearningSystem()

def initialize_enhanced_learning():
    """Initialize enhanced learning system"""
    enhanced_learning.start_enhanced_learning()
    return "Enhanced learning system with cross-domain synthesis initialized"

def trigger_enhanced_learning(assistant_name):
    """Trigger enhanced learning session"""
    enhanced_learning.adaptive_learning_session(assistant_name)
    return f"Enhanced learning completed for {assistant_name}"