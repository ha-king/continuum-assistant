import pytz
from datetime import datetime
import json
import boto3

class GlobalIntelligenceSystem:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.cultural_contexts = {
            'US': {
                'business_hours': (9, 17),
                'currency': 'USD',
                'date_format': '%m/%d/%Y',
                'cultural_notes': 'Direct communication, individual achievement focus'
            },
            'UK': {
                'business_hours': (9, 17),
                'currency': 'GBP',
                'date_format': '%d/%m/%Y',
                'cultural_notes': 'Polite indirectness, understatement common'
            },
            'JP': {
                'business_hours': (9, 18),
                'currency': 'JPY',
                'date_format': '%Y/%m/%d',
                'cultural_notes': 'Consensus building, respect for hierarchy'
            },
            'DE': {
                'business_hours': (8, 17),
                'currency': 'EUR',
                'date_format': '%d.%m.%Y',
                'cultural_notes': 'Precision, punctuality, direct communication'
            },
            'CN': {
                'business_hours': (9, 18),
                'currency': 'CNY',
                'date_format': '%Y-%m-%d',
                'cultural_notes': 'Relationship building, face-saving important'
            }
        }
        
        self.market_sessions = {
            'US': {'open': '09:30', 'close': '16:00', 'timezone': 'America/New_York'},
            'UK': {'open': '08:00', 'close': '16:30', 'timezone': 'Europe/London'},
            'JP': {'open': '09:00', 'close': '15:00', 'timezone': 'Asia/Tokyo'},
            'HK': {'open': '09:30', 'close': '16:00', 'timezone': 'Asia/Hong_Kong'},
            'AU': {'open': '10:00', 'close': '16:00', 'timezone': 'Australia/Sydney'}
        }
    
    def get_global_market_status(self):
        """Get current global market status"""
        current_utc = datetime.now(pytz.UTC)
        market_status = "🌍 **Global Market Status:**\n\n"
        
        for market, info in self.market_sessions.items():
            tz = pytz.timezone(info['timezone'])
            local_time = current_utc.astimezone(tz)
            
            # Parse market hours
            open_hour, open_min = map(int, info['open'].split(':'))
            close_hour, close_min = map(int, info['close'].split(':'))
            
            market_open = local_time.replace(hour=open_hour, minute=open_min, second=0, microsecond=0)
            market_close = local_time.replace(hour=close_hour, minute=close_min, second=0, microsecond=0)
            
            if market_open <= local_time <= market_close and local_time.weekday() < 5:
                status = "🟢 OPEN"
            else:
                status = "🔴 CLOSED"
            
            market_status += f"**{market}**: {status} | Local: {local_time.strftime('%H:%M %Z')}\n"
        
        return market_status
    
    def get_timezone_intelligence(self, user_timezone='UTC'):
        """Get timezone-aware business intelligence"""
        try:
            user_tz = pytz.timezone(user_timezone)
            current_time = datetime.now(user_tz)
            
            intelligence = f"⏰ **Timezone Intelligence:**\n\n"
            intelligence += f"Your local time: {current_time.strftime('%A, %B %d, %Y at %I:%M %p %Z')}\n\n"
            
            # Business hours analysis
            hour = current_time.hour
            if 9 <= hour <= 17:
                intelligence += "✅ **Business Hours**: Optimal time for professional communications\n"
            elif 6 <= hour < 9:
                intelligence += "🌅 **Early Hours**: Good for focused work, limited communications\n"
            elif 17 < hour <= 22:
                intelligence += "🌆 **Evening**: After-hours, consider urgency for communications\n"
            else:
                intelligence += "🌙 **Off Hours**: Non-business time, emergency communications only\n"
            
            # Global coordination suggestions
            intelligence += "\n**Global Coordination:**\n"
            
            # Find overlapping business hours with major markets
            overlaps = []
            for market, info in self.market_sessions.items():
                market_tz = pytz.timezone(info['timezone'])
                market_time = current_time.astimezone(market_tz)
                market_hour = market_time.hour
                
                open_hour = int(info['open'].split(':')[0])
                close_hour = int(info['close'].split(':')[0])
                
                if open_hour <= market_hour <= close_hour and market_time.weekday() < 5:
                    overlaps.append(f"{market} ({market_time.strftime('%H:%M %Z')})")
            
            if overlaps:
                intelligence += f"🤝 Active markets: {', '.join(overlaps)}\n"
            else:
                intelligence += "😴 No major markets currently active\n"
            
            return intelligence
            
        except Exception as e:
            return f"Timezone intelligence error: {str(e)}"
    
    def get_cultural_adaptation(self, region='US', business_context=''):
        """Get culturally adapted business intelligence"""
        if region not in self.cultural_contexts:
            region = 'US'  # Default fallback
        
        context = self.cultural_contexts[region]
        
        adaptation = f"🌏 **Cultural Business Intelligence - {region}:**\n\n"
        adaptation += f"**Currency**: {context['currency']}\n"
        adaptation += f"**Business Hours**: {context['business_hours'][0]}:00 - {context['business_hours'][1]}:00\n"
        adaptation += f"**Cultural Notes**: {context['cultural_notes']}\n\n"
        
        # Add region-specific business insights
        if region == 'JP':
            adaptation += "**Business Etiquette**:\n"
            adaptation += "• Bow slightly when greeting\n"
            adaptation += "• Exchange business cards with both hands\n"
            adaptation += "• Allow for consensus-building time in decisions\n"
        elif region == 'DE':
            adaptation += "**Business Etiquette**:\n"
            adaptation += "• Be punctual - arrive exactly on time\n"
            adaptation += "• Use formal titles and surnames\n"
            adaptation += "• Prepare detailed, fact-based presentations\n"
        elif region == 'CN':
            adaptation += "**Business Etiquette**:\n"
            adaptation += "• Build relationships before business discussions\n"
            adaptation += "• Avoid causing loss of face in public\n"
            adaptation += "• Respect hierarchy and seniority\n"
        
        return adaptation
    
    def predict_user_needs(self, user_history, current_context):
        """Predict user needs based on patterns"""
        try:
            prediction_prompt = f"""
            Based on user interaction history and current context, predict likely next queries:
            
            Recent queries: {user_history[-5:] if user_history else 'No history'}
            Current context: {current_context}
            Current time: {datetime.now().strftime('%A %H:%M UTC')}
            
            Predict 3 most likely next questions this user might ask, considering:
            - Time of day patterns
            - Topic progression
            - Business context
            - Market conditions
            
            Format as: "You might want to ask:"
            """
            
            response = self.bedrock.invoke_model(
                modelId="us.amazon.nova-micro-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": prediction_prompt}],
                    "max_tokens": 200,
                    "temperature": 0.4
                })
            )
            
            result = json.loads(response['body'].read())
            predictions = result.get('content', [{}])[0].get('text', '')
            
            return f"🔮 **Predictive Suggestions:**\n{predictions}"
            
        except Exception as e:
            return f"Prediction error: {str(e)}"

# Global instance
global_intel = GlobalIntelligenceSystem()

def get_global_market_status():
    """Get global market status"""
    return global_intel.get_global_market_status()

def get_timezone_intelligence(user_timezone='UTC'):
    """Get timezone-aware intelligence"""
    return global_intel.get_timezone_intelligence(user_timezone)

def get_cultural_adaptation(region='US', context=''):
    """Get cultural business adaptation"""
    return global_intel.get_cultural_adaptation(region, context)

def predict_user_needs(user_history, current_context):
    """Predict user needs"""
    return global_intel.predict_user_needs(user_history, current_context)