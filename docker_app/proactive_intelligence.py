import boto3
import json
from datetime import datetime, timedelta
import threading
import time

class ProactiveIntelligence:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.alert_subscribers = {}
        self.trend_monitors = {}
        self.risk_assessments = {}
        
    def monitor_market_trends(self):
        """Monitor and analyze market trends proactively"""
        try:
            trend_analysis_prompt = """
            Analyze current market trends across:
            1. Cryptocurrency markets (Bitcoin, Ethereum, major altcoins)
            2. Traditional financial markets (S&P 500, bonds, commodities)
            3. Geopolitical developments affecting markets
            4. Technology sector developments
            
            Identify:
            - Emerging trends (last 24 hours)
            - Risk factors requiring attention
            - Opportunities for strategic positioning
            
            Format: TREND: [description] | IMPACT: [high/medium/low] | TIMEFRAME: [immediate/short/long]
            """
            
            response = self.bedrock.invoke_model(
                modelId="us.amazon.nova-micro-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": trend_analysis_prompt}],
                    "max_tokens": 400,
                    "temperature": 0.2
                })
            )
            
            result = json.loads(response['body'].read())
            trends = result.get('content', [{}])[0].get('text', '')
            
            # Process and categorize trends
            self.process_trend_analysis(trends)
            
            return trends
            
        except Exception as e:
            print(f"Trend monitoring error: {str(e)}")
            return ""
    
    def process_trend_analysis(self, trends_text):
        """Process trend analysis and generate alerts"""
        lines = trends_text.split('\n')
        high_impact_trends = []
        
        for line in lines:
            if 'IMPACT: high' in line.lower():
                high_impact_trends.append(line)
        
        if high_impact_trends:
            alert_message = f"🚨 HIGH IMPACT TRENDS DETECTED:\n" + "\n".join(high_impact_trends)
            self.send_proactive_alert("market_trends", alert_message)
    
    def generate_daily_intelligence_brief(self):
        """Generate comprehensive daily intelligence briefing"""
        try:
            brief_prompt = f"""
            Generate a concise daily intelligence briefing for {datetime.now().strftime('%Y-%m-%d')}:
            
            EXECUTIVE SUMMARY:
            - Top 3 market developments
            - Key regulatory/policy changes
            - Technology/innovation highlights
            - Geopolitical risk factors
            
            STRATEGIC IMPLICATIONS:
            - Investment considerations
            - Risk mitigation priorities
            - Opportunity identification
            
            OUTLOOK:
            - Next 24-48 hour watch items
            - Week ahead key events
            
            Keep concise but actionable.
            """
            
            response = self.bedrock.invoke_model(
                modelId="us.amazon.nova-lite-v1:0",  # Slightly more capable for comprehensive analysis
                body=json.dumps({
                    "messages": [{"role": "user", "content": brief_prompt}],
                    "max_tokens": 500,
                    "temperature": 0.1
                })
            )
            
            result = json.loads(response['body'].read())
            brief = result.get('content', [{}])[0].get('text', '')
            
            # Store and distribute brief
            self.distribute_intelligence_brief(brief)
            
            return brief
            
        except Exception as e:
            print(f"Intelligence brief error: {str(e)}")
            return ""
    
    def assess_cross_domain_risks(self):
        """Assess risks across multiple domains"""
        try:
            risk_prompt = """
            Conduct cross-domain risk assessment:
            
            FINANCIAL RISKS:
            - Market volatility indicators
            - Liquidity concerns
            - Credit/counterparty risks
            
            GEOPOLITICAL RISKS:
            - Trade war escalation
            - Regulatory crackdowns
            - Sanctions/policy changes
            
            TECHNOLOGY RISKS:
            - Cybersecurity threats
            - Infrastructure vulnerabilities
            - Innovation disruption
            
            INTERCONNECTED RISKS:
            - How risks amplify across domains
            - Systemic risk factors
            - Cascade effect potential
            
            Rate each risk: LOW/MEDIUM/HIGH/CRITICAL
            """
            
            response = self.bedrock.invoke_model(
                modelId="us.amazon.nova-micro-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": risk_prompt}],
                    "max_tokens": 400,
                    "temperature": 0.1
                })
            )
            
            result = json.loads(response['body'].read())
            risk_assessment = result.get('content', [{}])[0].get('text', '')
            
            # Check for critical risks
            if 'CRITICAL' in risk_assessment.upper():
                self.send_proactive_alert("critical_risk", f"🔴 CRITICAL RISK DETECTED:\n{risk_assessment}")
            
            return risk_assessment
            
        except Exception as e:
            print(f"Risk assessment error: {str(e)}")
            return ""
    
    def predict_market_scenarios(self):
        """Generate predictive market scenarios"""
        try:
            scenario_prompt = """
            Generate 3 market scenarios for the next 30 days:
            
            SCENARIO 1 - BULLISH (30% probability):
            - Key drivers and catalysts
            - Expected market movements
            - Strategic positioning
            
            SCENARIO 2 - NEUTRAL (50% probability):
            - Sideways market factors
            - Range-bound expectations
            - Defensive strategies
            
            SCENARIO 3 - BEARISH (20% probability):
            - Risk factors and triggers
            - Downside protection needs
            - Crisis response plans
            
            Include specific actionable recommendations for each scenario.
            """
            
            response = self.bedrock.invoke_model(
                modelId="us.amazon.nova-lite-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": scenario_prompt}],
                    "max_tokens": 600,
                    "temperature": 0.3
                })
            )
            
            result = json.loads(response['body'].read())
            scenarios = result.get('content', [{}])[0].get('text', '')
            
            return scenarios
            
        except Exception as e:
            print(f"Scenario prediction error: {str(e)}")
            return ""
    
    def send_proactive_alert(self, alert_type, message):
        """Send proactive alerts to subscribers"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': timestamp,
            'priority': 'high' if 'CRITICAL' in message else 'medium'
        }
        
        print(f"🚨 PROACTIVE ALERT [{alert_type.upper()}]: {message}")
        
        # Store alert for user retrieval
        if alert_type not in self.alert_subscribers:
            self.alert_subscribers[alert_type] = []
        self.alert_subscribers[alert_type].append(alert)
        
        # Keep only last 10 alerts per type
        if len(self.alert_subscribers[alert_type]) > 10:
            self.alert_subscribers[alert_type] = self.alert_subscribers[alert_type][-10:]
    
    def distribute_intelligence_brief(self, brief):
        """Distribute daily intelligence brief"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        print(f"📊 DAILY INTELLIGENCE BRIEF [{timestamp}]:\n{brief}")
        
        # Store for user access
        self.trend_monitors[timestamp] = brief
    
    def get_recent_alerts(self, alert_type=None, limit=5):
        """Get recent proactive alerts"""
        if alert_type:
            return self.alert_subscribers.get(alert_type, [])[-limit:]
        else:
            all_alerts = []
            for alerts in self.alert_subscribers.values():
                all_alerts.extend(alerts)
            return sorted(all_alerts, key=lambda x: x['timestamp'])[-limit:]
    
    def get_latest_intelligence_brief(self):
        """Get the latest intelligence brief"""
        if not self.trend_monitors:
            return "No intelligence brief available yet."
        
        latest_date = max(self.trend_monitors.keys())
        return f"Intelligence Brief - {latest_date}:\n{self.trend_monitors[latest_date]}"
    
    def start_proactive_monitoring(self):
        """Start proactive intelligence monitoring"""
        def monitoring_loop():
            while True:
                try:
                    # Market trend monitoring every 2 hours
                    if datetime.now().minute == 0 and datetime.now().hour % 2 == 0:
                        self.monitor_market_trends()
                    
                    # Risk assessment every 6 hours
                    if datetime.now().minute == 0 and datetime.now().hour % 6 == 0:
                        self.assess_cross_domain_risks()
                    
                    # Daily intelligence brief at 8 AM
                    if datetime.now().hour == 8 and datetime.now().minute == 0:
                        self.generate_daily_intelligence_brief()
                    
                    # Scenario analysis twice daily
                    if datetime.now().hour in [9, 17] and datetime.now().minute == 0:
                        self.predict_market_scenarios()
                    
                    time.sleep(60)  # Check every minute
                    
                except Exception as e:
                    print(f"Proactive monitoring error: {str(e)}")
                    time.sleep(300)  # Wait 5 minutes on error
        
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
        print("Proactive intelligence monitoring started")

# Global instance
proactive_intel = ProactiveIntelligence()

def initialize_proactive_intelligence():
    """Initialize proactive intelligence system"""
    proactive_intel.start_proactive_monitoring()
    return "Proactive intelligence system initialized"

def get_proactive_alerts(alert_type=None):
    """Get recent proactive alerts"""
    return proactive_intel.get_recent_alerts(alert_type)

def get_intelligence_brief():
    """Get latest intelligence brief"""
    return proactive_intel.get_latest_intelligence_brief()

def trigger_market_analysis():
    """Manually trigger market trend analysis"""
    return proactive_intel.monitor_market_trends()