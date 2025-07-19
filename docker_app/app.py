import streamlit as st
import os
from strands import Agent
from strands_tools import file_read, file_write, editor, use_llm, memory, mem0_memory
from model_options import get_model_options, get_default_model
from auto_learning_system import initialize_auto_learning, trigger_manual_learning
from enhanced_learning_system import initialize_enhanced_learning, trigger_enhanced_learning
from personalized_intelligence import get_personalized_response, get_user_insights
from proactive_intelligence import initialize_proactive_intelligence, get_proactive_alerts, get_intelligence_brief, trigger_market_analysis
# Import lazy loading wrapper
from lazy_assistant import LazyAssistant

# Lazy load assistants to improve startup time
# Consolidated assistants
financial_assistant = LazyAssistant('consolidated_assistants', 'financial_assistant')
security_assistant = LazyAssistant('consolidated_assistants', 'security_assistant')
business_assistant = LazyAssistant('consolidated_assistants', 'business_assistant')
tech_assistant = LazyAssistant('consolidated_assistants', 'tech_assistant')
research_assistant = LazyAssistant('consolidated_assistants', 'research_assistant')
sports_assistant = LazyAssistant('consolidated_assistants', 'sports_assistant')
# Formula 1 assistant
formula1_assistant = LazyAssistant('formula1_assistant', 'formula1_assistant')
# Core assistants
english_assistant = LazyAssistant('english_assistant', 'english_assistant')
math_assistant = LazyAssistant('math_assistant', 'math_assistant')
aws_assistant = LazyAssistant('aws_assistant', 'aws_assistant')
louisiana_legal_assistant = LazyAssistant('louisiana_legal_assistant', 'louisiana_legal_assistant')
general_assistant = LazyAssistant('no_expertise', 'general_assistant')
universal_assistant = LazyAssistant('universal_assistant', 'universal_assistant')
aviation_assistant = LazyAssistant('aviation_assistant', 'aviation_assistant')
aviation_assistant_claude = LazyAssistant('claude_aviation_assistant', 'aviation_assistant_claude')
# Legacy assistants (now consolidated)
web_browser_assistant = LazyAssistant('web_browser_assistant', 'web_browser_assistant')
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
    
    # Provide context without specific dates that confuse the model
    context = "You have access to current real-time market data.\n"
    
    location = st.session_state.get('user_location')
    if location:
        context += f"User location: Latitude {location['latitude']:.4f}, Longitude {location['longitude']:.4f}\n"
    
    return context + "\n"

TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, an AI orchestrator with real-time data access and PREDICTION capabilities.

AVAILABLE ASSISTANTS:
- Math Assistant: calculations and mathematical problems
- English Assistant: writing, grammar, literature
- Financial Assistant: finance, crypto, economics, market analysis
- AWS Assistant: cloud architecture and best practices
- Business Assistant: business development, networking, company intelligence
- Tech Assistant: programming, AI, blockchain, web3
- Security Assistant: cybersecurity, cryptography, threat analysis
- Formula 1 Assistant: F1 racing with live data from multiple sources (OpenF1, Ergast, ESPN)
- Sports Assistant: general sports and motorsports
- Research Assistant: internet research with real-time data access
- Louisiana Legal Assistant: Louisiana business law
- Web Browser Assistant: website browsing and analysis
- Aviation Assistant: flight data, FAA information, air traffic
- Universal Assistant: ANY topic with prediction/forecasting capabilities
- General Assistant: other topics

ROUTING RULES:
1. For PREDICTION/FORECASTING queries (predict, forecast, will, future, next, expect), use Universal Assistant
2. For F1/Formula 1/racing queries, use Formula 1 Assistant
3. For AVIATION/FLIGHT queries (aircraft, flight, N628TS, N-numbers, airport, where is N), use Aviation Assistant
4. For current/real-time queries, use Research or Web Browser assistants
5. For topics without specific assistants, use Universal Assistant
6. Route to most appropriate specialist assistant for known domains

The Universal Assistant can handle predictions for ANY topic using historical + real-time data.
"""

def determine_action(agent, query):
    query_lower = query.lower()
    knowledge_keywords = ['remember', 'store', 'my birthday', 'personal', 'save this']
    if any(keyword in query_lower for keyword in knowledge_keywords):
        return "knowledge"
    return "teacher"

from batch_knowledge import store_knowledge_batch, flush_knowledge_queue

def store_knowledge(content, query_context):
    """Store non-redundant information in knowledge base using batch processing"""
    store_knowledge_batch(content, query_context)

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

def initialize_session_state():
    """Initialize all session state variables in one place"""
    if "tab_ids" not in st.session_state:
        st.session_state.tab_ids = [0]
    if "next_tab_id" not in st.session_state:
        st.session_state.next_tab_id = 1
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 0
    if "tab_messages" not in st.session_state:
        st.session_state.tab_messages = {}

# Initialize session state
initialize_session_state()

col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
with col1:
    tab_names = [f"Chat {tid+1}" for tid in st.session_state.tab_ids]
    tabs = st.tabs(tab_names)
    # Set active tab when clicked
    for i, _ in enumerate(tabs):
        if i < len(tab_names):
            st.session_state.active_tab = i
with col2:
    if st.button("+ Tab"):
        st.session_state.tab_ids.append(st.session_state.next_tab_id)
        st.session_state.next_tab_id += 1
        st.session_state.active_tab = len(st.session_state.tab_ids) - 1
        st.rerun()
with col3:
    if st.button("✕ Close") and len(st.session_state.tab_ids) > 1:
        # Remove the active tab
        active_idx = st.session_state.active_tab
        tab_id = st.session_state.tab_ids.pop(active_idx)
        # Clean up messages for this tab
        if tab_id in st.session_state.tab_messages:
            del st.session_state.tab_messages[tab_id]
        # Update active tab index
        st.session_state.active_tab = min(active_idx, len(st.session_state.tab_ids) - 1)
        st.rerun()
with col4:
    # Display active tab indicator
    st.write(f"Tab: {st.session_state.active_tab + 1}")

with st.sidebar:
    # Add logout button
    if st.button("🚪 Logout"):
        authenticator.logout()
        st.rerun()
    
    st.header("Configuration")
    
    # Get model options from centralized configuration
    model_options = get_model_options()
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

teacher_tools = []
if use_math:
    teacher_tools.append(math_assistant)
if use_english:
    teacher_tools.append(english_assistant)
if use_financial or use_cryptocurrency or use_economics:
    teacher_tools.append(financial_assistant)
if use_aws:
    teacher_tools.append(aws_assistant)
if use_business_dev or use_entrepreneurship:
    teacher_tools.append(business_assistant)
if use_cs or use_ai or use_blockchain:
    teacher_tools.append(tech_assistant)
if use_cybersec_defense:
    teacher_tools.append(security_assistant)
# Include sports assistant and formula1 assistant for F1 queries
teacher_tools.append(sports_assistant)
teacher_tools.append(formula1_assistant)  # Add Formula 1 assistant
if use_research:
    teacher_tools.append(research_assistant)
if use_louisiana_legal:
    teacher_tools.append(louisiana_legal_assistant)
if use_web_browser:
    teacher_tools.append(web_browser_assistant)
if use_general:
    teacher_tools.append(general_assistant)
    teacher_tools.append(universal_assistant)  # Always include universal assistant
    teacher_tools.append(aviation_assistant)  # Always include aviation assistant

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
                        from smart_router import smart_route
                        
                        # Smart routing with priority-based logic
                        # Use Claude 4.0 for aviation if selected
                        use_claude = selected_model == "anthropic.claude-4-0:0"
                        
                        assistants = {
                            'aviation': aviation_assistant_claude if use_claude else aviation_assistant,
                            'sports': sports_assistant,
                            'formula1': formula1_assistant,  # Add Formula 1 assistant
                            'financial': financial_assistant,
                            'web_browser': web_browser_assistant,
                            'research': research_assistant
                        }
                        
                        assistant_func, enhanced_prompt = smart_route(prompt, get_current_datetime(), assistants)
                        
                        if assistant_func:
                            content = assistant_func(enhanced_prompt)
                        elif enhanced_prompt:
                            content = enhanced_prompt  # Direct response (like time queries)
                        else:
                            # Default to teacher agent with streaming
                            from streaming import get_streaming_response
                            teacher_agent = create_teacher_agent_with_datetime()
                            content = get_streaming_response(teacher_agent, full_prompt)
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
                    
                    # Clean the response to remove routing information
                    from response_cleaner import clean_response
                    cleaned_content = clean_response(personalized_content)
                    
                    # Display cleaned personalized content
                    st.markdown(cleaned_content)
                    
                    # Add expandable reference section if references exist
                    if "**References Used:**" in content:
                        with st.expander("📚 View References & Assistant Details"):
                            ref_start = content.find("**References Used:**")
                            if ref_start != -1:
                                references = content[ref_start:]
                                st.markdown(references)
                                st.markdown(f"**Assistant Used:** {action.title()} Mode")
                    
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": cleaned_content})
                    
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