import streamlit as st
import os
from strands import Agent
from strands_tools import file_read, file_write, editor, use_llm, memory, mem0_memory
from auto_learning_system import initialize_auto_learning, trigger_manual_learning
from enhanced_learning_system import initialize_enhanced_learning, trigger_enhanced_learning
from personalized_intelligence import get_personalized_response, get_user_insights
from proactive_intelligence import initialize_proactive_intelligence, get_proactive_alerts, get_intelligence_brief, trigger_market_analysis
# Consolidated assistants
from consolidated_assistants import (
    financial_assistant, security_assistant, business_assistant,
    tech_assistant, research_assistant
)
# Core assistants
from english_assistant import english_assistant
from math_assistant import math_assistant
from aws_assistant import aws_assistant
from louisiana_legal_assistant import louisiana_legal_assistant
from no_expertise import general_assistant
# Legacy assistants (now consolidated)
from web_browser_assistant import web_browser_assistant
from utils.auth import Auth
from config_file import Config

# Authentication setup
if os.environ.get("LOCAL_DEV"):
    st.write("🔓 **Local Development Mode** - Authentication bypassed")
else:
    try:
        # Detect environment from environment variable or default to prod
        env = os.environ.get("ENVIRONMENT", "prod")
        secret_id = Config.get_secrets_manager_id(env)
        
        authenticator = Auth.get_authenticator(
            secret_id=secret_id,
            region=Config.DEPLOYMENT_REGION
        )
        
        # Check authentication
        is_logged_in = authenticator.login()
        
        if not is_logged_in:
            st.stop()
            
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.stop()

def get_current_datetime():
    """Get current datetime formatted for user's timezone"""
    from datetime import datetime
    import pytz
    
    # Force current actual datetime
    current_time = datetime.now()
    
    user_tz = st.session_state.get('user_timezone', 'UTC')
    try:
        tz = pytz.timezone(user_tz)
        user_time = current_time.astimezone(tz)
        return user_time.strftime("%A, %B %d, %Y at %I:%M %p %Z")
    except:
        return current_time.strftime("%A, %B %d, %Y at %I:%M %p UTC")

def get_user_context():
    """Get user context including location and timezone"""
    from datetime import datetime
    
    # Ensure we always use actual current time
    actual_current_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p UTC")
    context = f"IMPORTANT: Current actual date and time is {actual_current_time}\n"
    context += f"User's local time: {get_current_datetime()}\n"
    
    location = st.session_state.get('user_location')
    if location:
        context += f"User location: Latitude {location['latitude']:.4f}, Longitude {location['longitude']:.4f}\n"
    
    return context + "\n"

TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, an AI orchestrator with real-time data access.

AVAILABLE ASSISTANTS:
- Math Assistant: calculations and mathematical problems
- English Assistant: writing, grammar, literature
- Financial Assistant: finance, crypto, economics, market analysis
- AWS Assistant: cloud architecture and best practices
- Business Assistant: business development, networking, company intelligence
- Tech Assistant: programming, AI, blockchain, web3
- Security Assistant: cybersecurity, cryptography, threat analysis
- Research Assistant: internet research with real-time data access
- Louisiana Legal Assistant: Louisiana business law
- Web Browser Assistant: website browsing and analysis
- General Assistant: other topics

Route queries to the most appropriate assistant based on the topic.
For current/real-time queries, use Research or Web Browser assistants.
"""

def determine_action(agent, query):
    query_lower = query.lower()
    knowledge_keywords = ['remember', 'store', 'my birthday', 'personal', 'save this']
    if any(keyword in query_lower for keyword in knowledge_keywords):
        return "knowledge"
    return "teacher"

def store_knowledge(content, query_context):
    """Store non-redundant information in knowledge base"""
    if not os.environ.get("KNOWLEDGE_BASE_ID"):
        return
    
    try:
        agent = Agent(tools=[memory, use_llm])
        
        # Check for existing similar content
        existing = agent.tool.memory(action="retrieve", query=content[:100], min_score=0.8, max_results=3)
        
        # Only store if not redundant
        if not existing or len(str(existing).strip()) < 50:
            agent.tool.memory(action="store", content=f"{query_context}\nLearned: {content}")
    except Exception:
        pass

def run_kb_agent(query, datetime_context):
    if not os.environ.get("KNOWLEDGE_BASE_ID"):
        return "Knowledge base is not configured. Please use the teacher mode for educational questions."
    
    try:
        agent = Agent(tools=[memory, use_llm])
        
        if "remember" in query.lower() or "store" in query.lower():
            agent.tool.memory(action="store", content=query)
            return "I've stored this information."
        else:
            result = agent.tool.memory(action="retrieve", query=query, min_score=0.4, max_results=9)
            answer = agent.tool.use_llm(
                prompt=f"{datetime_context}User question: \"{query}\"\n\nInformation: {str(result)}\n\nProvide a helpful answer:",
                system_prompt="You are a helpful knowledge assistant that provides clear, concise answers based on information retrieved from a knowledge base."
            )
            
            # Store new knowledge from the response
            store_knowledge(str(answer), f"Query: {query}")
            
            return str(answer)
    except Exception:
        return "Knowledge base is not configured. Please use the teacher mode for educational questions."

def run_memory_agent(query, datetime_context):
    agent = Agent(system_prompt=f"You are a personal assistant that maintains context by remembering user details. {datetime_context}", tools=[mem0_memory, use_llm])
    response = agent(query)
    return str(response)

st.title("🔒 Son of Anton")

# Initialize enhanced intelligence systems
if 'intelligence_initialized' not in st.session_state:
    auto_status = initialize_auto_learning()
    enhanced_status = initialize_enhanced_learning()
    proactive_status = initialize_proactive_intelligence()
    st.session_state.intelligence_initialized = True
    st.success("🤖 Advanced Intelligence Systems Active")
    st.info("✨ Cross-domain synthesis, personalization, and proactive monitoring enabled")

# Get user's timezone and geolocation from browser JavaScript
if 'user_timezone' not in st.session_state or 'user_location' not in st.session_state:
    st.components.v1.html("""
    <script>
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    window.parent.postMessage({type: 'timezone', value: timezone}, '*');
    
    // Get geolocation if available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const location = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
                window.parent.postMessage({type: 'location', value: location}, '*');
            },
            function(error) {
                window.parent.postMessage({type: 'location', value: null}, '*');
            }
        );
    }
    </script>
    """, height=0)
    
    # Set defaults
    st.session_state.user_timezone = 'UTC'
    st.session_state.user_location = None

if "tab_ids" not in st.session_state:
    st.session_state.tab_ids = [0]
if "next_tab_id" not in st.session_state:
    st.session_state.next_tab_id = 1

col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    tab_names = [f"Chat {tid+1}" for tid in st.session_state.tab_ids]
    tabs = st.tabs(tab_names)
with col2:
    if st.button("+ Tab"):
        st.session_state.tab_ids.append(st.session_state.next_tab_id)
        st.session_state.next_tab_id += 1
        st.rerun()
with col3:
    if st.button("✕ Close") and len(st.session_state.tab_ids) > 1:
        st.session_state.tab_ids.pop()
        st.rerun()

with st.sidebar:
    # Add logout button
    if st.button("🚪 Logout"):
        authenticator.logout()
        st.rerun()
    
    st.header("Configuration")
    
    model_options = [
        "us.amazon.nova-pro-v1:0",
        "us.amazon.nova-lite-v1:0", 
        "us.amazon.nova-micro-v1:0",
        "anthropic.claude-3-5-haiku-20241022-v1:0",
        "anthropic.claude-3-5-sonnet-20241022-v1:0",
        "anthropic.claude-3-opus-20240229-v1:0"
    ]
    selected_model = st.selectbox("Bedrock Model:", model_options)
    
    opensearch_available = bool(os.environ.get("OPENSEARCH_HOST"))
    memory_options = ["Bedrock Knowledge Base"]
    if opensearch_available:
        memory_options.append("OpenSearch Memory")
    
    memory_backend = st.selectbox("Memory Backend:", memory_options)
    
    assistant_mode = st.selectbox(
        "Assistant Mode:",
        ["All Assistants (Auto-Route)", "Advanced Configuration"]
    )
    
    if assistant_mode == "Advanced Configuration":
        with st.expander("🎯 Core Assistants", expanded=False):
            use_math = st.checkbox("Math", value=True)
            use_english = st.checkbox("English", value=True)
            use_cs = st.checkbox("Computer Science", value=True)
            use_financial = st.checkbox("Financial", value=True)
            use_aws = st.checkbox("AWS", value=True)
            use_research = st.checkbox("Research", value=True)
            use_web_browser = st.checkbox("Web Browser", value=True)
        
        with st.expander("🏢 Business & Finance", expanded=False):
            use_business_dev = st.checkbox("Business Development", value=True)
            use_business_contact = st.checkbox("Business Contacts", value=True)
            use_company_intelligence = st.checkbox("Company Intelligence", value=True)
            use_economics = st.checkbox("Economics", value=True)
            use_entrepreneurship = st.checkbox("Entrepreneurship", value=True)
        
        with st.expander("🌍 Global & Legal", expanded=False):
            use_geopolitical = st.checkbox("Geopolitical", value=True)
            use_international_finance = st.checkbox("International Finance", value=True)
            use_louisiana_legal = st.checkbox("Louisiana Legal", value=True)
            use_public_records = st.checkbox("Public Records", value=True)
        
        with st.expander("🔬 Technology & Security", expanded=False):
            use_ai = st.checkbox("AI", value=True)
            use_blockchain = st.checkbox("Blockchain", value=True)
            use_cryptocurrency = st.checkbox("Cryptocurrency", value=True)
            use_cybersec_defense = st.checkbox("Cybersecurity", value=True)
            use_data_analysis = st.checkbox("Data Analysis", value=True)
            use_predictive_analysis = st.checkbox("Predictive Analysis", value=True)
        
        # Set unused variables to False in advanced mode
        use_general = True
    else:
        # All assistants enabled in auto-route mode
        use_math = use_english = use_cs = use_financial = use_aws = True
        use_business_dev = use_research = use_louisiana_legal = True
        use_web_browser = use_general = True
        use_economics = use_entrepreneurship = use_ai = True
        use_blockchain = use_cryptocurrency = use_cybersec_defense = True
    
    st.divider()
    st.caption(f"Active Assistants: {sum([use_math, use_english, use_cs, use_financial, use_aws, use_business_dev, use_research, use_louisiana_legal, use_web_browser, use_general])}")
    
    with st.expander("📊 Intelligence Dashboard", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧠 Test Enhanced Learning"):
                result = trigger_enhanced_learning("financial_assistant")
                st.success(result)
            
            if st.button("📊 Market Analysis"):
                analysis = trigger_market_analysis()
                st.info(analysis[:300] + "..." if len(analysis) > 300 else analysis)
        
        with col2:
            if st.button("🚨 View Alerts"):
                alerts = get_proactive_alerts()
                if alerts:
                    for alert in alerts[-3:]:
                        st.warning(f"{alert['type']}: {alert['message'][:100]}...")
                else:
                    st.info("No recent alerts")
            
            if st.button("📝 Intelligence Brief"):
                brief = get_intelligence_brief()
                st.text_area("Daily Brief", brief[:500] + "..." if len(brief) > 500 else brief, height=150)


st.write("🔐 **Authenticated Access** - Ask a question in any subject area, and I'll route it to the appropriate specialist.")

teacher_tools = []
if use_math:
    teacher_tools.append(math_assistant)
if use_english:
    teacher_tools.append(english_assistant)
if use_financial or use_cryptocurrency or use_economics:
    teacher_tools.append(financial_assistant)
if use_aws:
    teacher_tools.append(aws_assistant)
if use_business_dev or use_entrepreneurship or use_professional_networking:
    teacher_tools.append(business_assistant)
if use_cs or use_ai or use_blockchain or use_web3:
    teacher_tools.append(tech_assistant)
if use_cybersec_defense or use_cybersec_offense or use_cryptography:
    teacher_tools.append(security_assistant)
if use_research:
    teacher_tools.append(research_assistant)
if use_louisiana_legal:
    teacher_tools.append(louisiana_legal_assistant)
if use_web_browser:
    teacher_tools.append(web_browser_assistant)
if use_general:
    teacher_tools.append(general_assistant)

# Create teacher agent with datetime awareness
def create_teacher_agent_with_datetime():
    from agent_pool import get_cached_agent
    
    user_context = get_user_context()
    enhanced_prompt = f"""{TEACHER_SYSTEM_PROMPT}

CONTEXT: {user_context}
Include current date/time when calling assistants.

For time/date queries, respond directly with current time.
"""
    return get_cached_agent(enhanced_prompt, teacher_tools)

teacher_agent = create_teacher_agent_with_datetime()

if "tab_messages" not in st.session_state:
    st.session_state.tab_messages = {}

for i, tab in enumerate(tabs):
    with tab:
        tab_id = st.session_state.tab_ids[i]
        if tab_id not in st.session_state.tab_messages:
            st.session_state.tab_messages[tab_id] = []
        
        if st.button("🗑️ Clear Chat", key=f"clear_{tab_id}"):
            st.session_state.tab_messages[tab_id] = []
            st.rerun()
        
        for message in st.session_state.tab_messages[tab_id]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input(f"Ask your question here... (Tab {tab_id+1})", key=f"chat_input_{tab_id}"):
            st.session_state.tab_messages[tab_id].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    # Get current datetime and user context for orchestrator and all agents
                    user_context = get_user_context()
                    datetime_context = user_context
                    
                    router_agent = Agent(tools=[use_llm])
                    action = determine_action(router_agent, prompt)
                    
                    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.tab_messages[tab_id][-10:]])
                    full_prompt = f"{datetime_context}Context: {context}\n\nCurrent question: {prompt}" if context else f"{datetime_context}Current question: {prompt}"
                    
                    # Store user query context for knowledge base
                    query_context = f"User query at {get_current_datetime()}: {prompt}"
                    
                    if action == "teacher":
                        # Handle direct time/date queries
                        time_keywords = ['what time', 'what day', 'current time', 'current date', 'time is it', 'day is it']
                        if any(keyword in prompt.lower() for keyword in time_keywords):
                            content = f"It is {get_current_datetime()}"
                        # Handle crypto price queries - route to cryptocurrency assistant
                        elif any(word in prompt.lower() for word in ['crypto', 'bitcoin', 'ethereum', 'apecoin', 'price', 'coinbase']):
                            content = financial_assistant(f"{datetime_context}{prompt}")
                        elif any(word in prompt.lower() for word in ['browse', 'infascination', '.com', 'website', 'visit', 'current', 'today', 'now', 'latest', 'real-time']):
                            try:
                                # Try web browser first, fallback to research assistant
                                if any(word in prompt.lower() for word in ['.com', 'website', 'browse', 'visit']):
                                    content = web_browser_assistant(f"{datetime_context}{prompt}")
                                else:
                                    content = research_assistant(f"{datetime_context}{prompt}")
                            except Exception as e:
                                try:
                                    content = research_assistant(f"{datetime_context}{prompt}")
                                except:
                                    response = teacher_agent(full_prompt)
                                    content = str(response)
                        else:
                            # Recreate teacher agent with fresh datetime for each request
                            teacher_agent = create_teacher_agent_with_datetime()
                            response = teacher_agent(full_prompt)
                            content = str(response)
                            
                            # Store knowledge from response
                            store_knowledge(content, query_context)
                    else:
                        if memory_backend == "OpenSearch Memory":
                            content = run_memory_agent(full_prompt, datetime_context)
                        else:
                            kb_result = run_kb_agent(full_prompt, datetime_context)
                            if "Knowledge base is not configured" in kb_result:
                                # Recreate teacher agent with fresh datetime for each request
                                teacher_agent = create_teacher_agent_with_datetime()
                                response = teacher_agent(full_prompt)
                                content = str(response)
                                
                                # Store knowledge from response
                                store_knowledge(content, query_context)
                            else:
                                content = kb_result
                    
                    # Get user ID for personalization
                    user_id = st.session_state.get('user_id', 'anonymous')
                    
                    # Apply personalization
                    personalized_content = get_personalized_response(user_id, prompt, content)
                    
                    # Display personalized content
                    st.markdown(personalized_content)
                    
                    # Add expandable reference section if references exist
                    if "**References Used:**" in content:
                        with st.expander("📚 View References & Assistant Details"):
                            ref_start = content.find("**References Used:**")
                            if ref_start != -1:
                                references = content[ref_start:]
                                st.markdown(references)
                                st.markdown(f"**Assistant Used:** {action.title()} Mode")
                    
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": personalized_content})
                    
                    # Show user insights in sidebar
                    if user_id != 'anonymous':
                        with st.sidebar:
                            with st.expander("👤 User Insights", expanded=False):
                                insights = get_user_insights(user_id)
                                st.json(insights)
                    
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": error_msg})