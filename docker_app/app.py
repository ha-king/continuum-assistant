import streamlit as st
import os
import time
from strands import Agent
from strands_tools import file_read, file_write, editor, use_llm, memory, mem0_memory
from model_options import get_model_options, get_default_model
from auto_learning_system import initialize_auto_learning, trigger_manual_learning
from enhanced_learning_system import initialize_enhanced_learning, trigger_enhanced_learning
from personalized_intelligence import get_personalized_response, get_user_insights
from proactive_intelligence import initialize_proactive_intelligence, get_proactive_alerts, get_intelligence_brief, trigger_market_analysis
# Import lazy loading wrapper
from lazy_assistant import LazyAssistant

# Lazy load unified core domain assistants
business_finance_assistant = LazyAssistant('unified_assistants', 'business_finance_assistant')
tech_security_assistant = LazyAssistant('unified_assistants', 'tech_security_assistant')
research_knowledge_assistant = LazyAssistant('unified_assistants', 'research_knowledge_assistant')
specialized_industries_assistant = LazyAssistant('unified_assistants', 'specialized_industries_assistant')
universal_assistant = LazyAssistant('unified_assistants', 'universal_assistant')

# Keep specialized assistants for direct routing
formula1_assistant = LazyAssistant('formula1_assistant', 'formula1_assistant')
aviation_assistant = LazyAssistant('aviation_assistant', 'aviation_assistant')
aviation_assistant_claude = LazyAssistant('claude_aviation_assistant', 'aviation_assistant_claude')

# Legacy assistants (for backward compatibility)
financial_assistant = LazyAssistant('consolidated_assistants', 'financial_assistant')
security_assistant = LazyAssistant('consolidated_assistants', 'security_assistant')
business_assistant = LazyAssistant('consolidated_assistants', 'business_assistant')
tech_assistant = LazyAssistant('consolidated_assistants', 'tech_assistant')
research_assistant = LazyAssistant('consolidated_assistants', 'research_assistant')
sports_assistant = LazyAssistant('consolidated_assistants', 'sports_assistant')
english_assistant = LazyAssistant('english_assistant', 'english_assistant')
math_assistant = LazyAssistant('math_assistant', 'math_assistant')
aws_assistant = LazyAssistant('aws_assistant', 'aws_assistant')
louisiana_legal_assistant = LazyAssistant('louisiana_legal_assistant', 'louisiana_legal_assistant')
general_assistant = LazyAssistant('no_expertise', 'general_assistant')
web_browser_assistant = LazyAssistant('web_browser_assistant', 'web_browser_assistant')
from utils.auth import Auth
from config_file import Config

# Import conversation storage
from conversation_storage import conversation_storage, load_user_conversation, save_user_conversation

# Authentication setup
if os.environ.get("LOCAL_DEV"):
    st.write("🔓 **Local Development Mode** - Authentication bypassed")
    # Set a default user ID for local development
    st.session_state.user_id = "local-dev-user"
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
        
        # Store user ID in session state for conversation persistence
        if 'user_id' not in st.session_state and authenticator.is_logged_in():
            username = authenticator.get_username()
            if username:
                st.session_state.user_id = username
                # Load user's conversation history
                load_user_conversation(st.session_state.user_id)
            
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
    """Get user context including location, timezone, and personal information"""
    from datetime import datetime
    from user_profile import get_personal_context
    
    # Provide context without specific dates that confuse the model
    context = "You have access to current real-time market data.\n"
    
    # Add geolocation if available
    location = st.session_state.get('user_location')
    if location:
        context += f"User location: Latitude {location['latitude']:.4f}, Longitude {location['longitude']:.4f}\n"
    
    # Add personal context if available
    user_id = st.session_state.get('user_id', 'anonymous')
    personal_context = get_personal_context(user_id)
    if personal_context:
        context += f"\n{personal_context}\n"
    
    return context + "\n"

from response_processor import process_response

# Import telemetry integration
try:
    from app_telemetry import (
        track_app_startup, track_user_query, track_assistant_response,
        track_router_decision, track_tab_change, track_error, TELEMETRY_ENABLED
    )
    if TELEMETRY_ENABLED:
        print("Telemetry enabled")
        track_app_startup()
except ImportError:
    # Create dummy functions if telemetry module is not available
    def track_app_startup(): pass
    def track_user_query(*args, **kwargs): pass
    def track_assistant_response(*args, **kwargs): pass
    def track_router_decision(*args, **kwargs): pass
    def track_tab_change(*args, **kwargs): pass
    def track_error(*args, **kwargs): pass
    TELEMETRY_ENABLED = False
    print("Telemetry disabled")

TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, an AI orchestrator with real-time data access and PREDICTION capabilities.

AVAILABLE CORE DOMAIN ASSISTANTS:
- Business & Finance Assistant: finance, crypto, economics, business development, entrepreneurship, investments
- Technology & Security Assistant: programming, AI, blockchain, web3, cybersecurity, AWS, cloud computing
- Research & Knowledge Assistant: internet research, data analysis, math, English, writing, general knowledge
- Specialized Industries Assistant: aviation, Formula 1, sports, legal, automotive industries
- Universal Assistant: predictions, forecasting, and general queries across all domains

SPECIALIZED ASSISTANTS (for specific queries):
- Formula 1 Assistant: F1 racing with live data from multiple sources (OpenF1, Ergast, ESPN)
- Aviation Assistant: flight data, FAA information, air traffic, aircraft tracking

ROUTING RULES:
1. For PREDICTION/FORECASTING queries (predict, forecast, will, future, next, expect), use Universal Assistant
2. For F1/Formula 1/racing queries, use Formula 1 Assistant
3. For AVIATION/FLIGHT queries (aircraft, flight, N-numbers, airport), use Aviation Assistant
4. For BUSINESS/FINANCE queries, use Business & Finance Assistant
5. For TECHNOLOGY/SECURITY queries, use Technology & Security Assistant
6. For RESEARCH/KNOWLEDGE queries, use Research & Knowledge Assistant
7. For topics without specific domain match, use Universal Assistant

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
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Initialize session state
initialize_session_state()

with st.sidebar:
    # Add logout button
    if st.button("🚪 Logout") and 'authenticator' in locals():
        authenticator.logout()
        # Clear user session data
        if 'user_id' in st.session_state:
            del st.session_state.user_id
        if 'messages' in st.session_state:
            st.session_state.messages = []
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
        ["Core Domains (Auto-Route)", "Advanced Configuration"]
    )
    
    if assistant_mode == "Advanced Configuration":
        with st.expander("🎯 Core Domain Assistants", expanded=True):
            use_business_finance = st.checkbox("Business & Finance", value=True)
            use_tech_security = st.checkbox("Technology & Security", value=True)
            use_research_knowledge = st.checkbox("Research & Knowledge", value=True)
            use_specialized_industries = st.checkbox("Specialized Industries", value=True)
            use_universal = st.checkbox("Universal", value=True)
        
        with st.expander("🔍 Legacy Assistants", expanded=False):
            use_math = st.checkbox("Math", value=False)
            use_english = st.checkbox("English", value=False)
            use_cs = st.checkbox("Computer Science", value=False)
            use_financial = st.checkbox("Financial", value=False)
            use_aws = st.checkbox("AWS", value=False)
            use_research = st.checkbox("Research", value=False)
            use_web_browser = st.checkbox("Web Browser", value=False)
            use_business_dev = st.checkbox("Business Development", value=False)
            use_business_contact = st.checkbox("Business Contacts", value=False)
            use_company_intelligence = st.checkbox("Company Intelligence", value=False)
            use_economics = st.checkbox("Economics", value=False)
            use_entrepreneurship = st.checkbox("Entrepreneurship", value=False)
            use_geopolitical = st.checkbox("Geopolitical", value=False)
            use_international_finance = st.checkbox("International Finance", value=False)
            use_louisiana_legal = st.checkbox("Louisiana Legal", value=False)
            use_public_records = st.checkbox("Public Records", value=False)
            use_ai = st.checkbox("AI", value=False)
            use_blockchain = st.checkbox("Blockchain", value=False)
            use_cryptocurrency = st.checkbox("Cryptocurrency", value=False)
            use_cybersec_defense = st.checkbox("Cybersecurity", value=False)
            use_data_analysis = st.checkbox("Data Analysis", value=False)
            use_predictive_analysis = st.checkbox("Predictive Analysis", value=False)
        
        # Set unused variables to False in advanced mode
        use_general = st.checkbox("General", value=False)
    else:
        # Core domain assistants enabled in auto-route mode
        use_business_finance = use_tech_security = use_research_knowledge = True
        use_specialized_industries = use_universal = True
        
        # Legacy assistants disabled in auto-route mode
        use_math = use_english = use_cs = use_financial = use_aws = False
        use_business_dev = use_research = use_louisiana_legal = False
        use_web_browser = use_general = False
        use_economics = use_entrepreneurship = use_ai = False
        use_blockchain = use_cryptocurrency = use_cybersec_defense = False
        use_business_contact = use_company_intelligence = use_geopolitical = False
        use_international_finance = use_public_records = False
        use_data_analysis = use_predictive_analysis = False
    
    st.divider()
    active_count = sum([use_business_finance, use_tech_security, use_research_knowledge, 
                        use_specialized_industries, use_universal])
    legacy_count = sum([use_math, use_english, use_cs, use_financial, use_aws, 
                        use_business_dev, use_research, use_louisiana_legal, 
                        use_web_browser, use_general])
    st.caption(f"Active Assistants: {active_count} core domains, {legacy_count} legacy")

# Initialize teacher tools with core domain assistants
teacher_tools = [
    business_finance_assistant,  # Core Domain 1: Business & Finance
    tech_security_assistant,     # Core Domain 2: Technology & Security
    research_knowledge_assistant, # Core Domain 3: Research & Knowledge
    specialized_industries_assistant, # Core Domain 4: Specialized Industries
    universal_assistant,         # Core Domain 5: Universal Assistant
    formula1_assistant,          # Specialized: Formula 1
    aviation_assistant           # Specialized: Aviation
]

# Add legacy assistants based on configuration if in advanced mode
if assistant_mode == "Advanced Configuration":
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

# Display chat interface
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    # Start a new conversation without deleting the old one
    user_id = st.session_state.get('user_id', 'anonymous')
    if user_id != 'anonymous':
        conversation_storage.start_new_conversation(user_id)
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your question here..."):
            # Get user ID for tracking
            user_id = st.session_state.get('user_id', 'anonymous')
            
            # Track user query
            track_user_query(user_id, prompt, 0)  # Use 0 as default tab_id
            
            # Extract and store personal information from message
            from user_profile import update_user_profile
            extracted_info = update_user_profile(user_id, prompt)
            
            # Add timestamp to user message for persistence
            message_with_timestamp = {
                "role": "user", 
                "content": prompt,
                "timestamp": int(time.time())
            }
            st.session_state.messages.append(message_with_timestamp)
            
            # Save conversation after user message
            save_user_conversation(user_id)
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    # Initialize variables to avoid undefined errors
                    enhanced_prompt = None
                    assistant_func = None
                    
                    # Get current datetime and user context for orchestrator and all agents
                    user_context = get_user_context()
                    datetime_context = user_context
                    
                    router_agent = Agent(tools=[use_llm])
                    action = determine_action(router_agent, prompt)
                    
                    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages[-10:]])
                    full_prompt = f"{datetime_context}Context: {context}\n\nCurrent question: {prompt}" if context else f"{datetime_context}Current question: {prompt}"
                    
                    # Store user query context for knowledge base
                    query_context = f"User query at {get_current_datetime()}: {prompt}"
                    
                    if action == "teacher":
                        from unified_router import unified_route
                        from response_cache import response_cache
                        
                        # Use Claude 4.0 for aviation if selected
                        use_claude = selected_model == "anthropic.claude-4-0:0"
                        
                        # Check cache first
                        cache_key = response_cache.get_cache_key(prompt, selected_model, user_id)
                        cached_response = response_cache.get(cache_key)
                        
                        if cached_response:
                            # Use cached response
                            content = cached_response
                            # Start timing for response time tracking (minimal since using cache)
                            start_time = time.time()
                        else:
                            # Start timing for response time tracking
                            start_time = time.time()
                            
                            # Map assistants to domains using the new unified structure
                            assistants = {
                                # Core domain assistants
                                'business_finance': business_finance_assistant,
                                'tech_security': tech_security_assistant,
                                'research_knowledge': research_knowledge_assistant,
                                'specialized_industries': specialized_industries_assistant,
                                'universal': universal_assistant,
                                
                                # Specialized assistants for direct routing
                                'aviation': aviation_assistant_claude if use_claude else aviation_assistant,
                                'formula1': formula1_assistant,
                                
                                # Legacy assistants for backward compatibility
                                'financial': financial_assistant,
                                'sports': sports_assistant,
                                'web_browser': web_browser_assistant,
                                'research': research_assistant
                            }
                            
                            # Unified routing with tracking
                            assistant_func, enhanced_prompt = unified_route(prompt, get_current_datetime(), assistants)
                            
                            # Track routing decision
                            if assistant_func:
                                assistant_name = assistant_func.__name__ if hasattr(assistant_func, "__name__") else str(assistant_func)
                                matched_rule = "direct" if assistant_name == "direct_response" else assistant_name.replace("_assistant", "")
                                track_router_decision(prompt, matched_rule, assistant_name, 0.8)
                            
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
                            
                            # Cache the response if it's not time-sensitive
                            if not any(time_term in prompt.lower() for time_term in ['time', 'date', 'today', 'now', 'current']):
                                response_cache.set(cache_key, content)
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
                    
                    # Process the response (clean and format)
                    user_data = {"user_id": user_id, "location": st.session_state.get('user_location')}
                    processed_content = process_response(personalized_content, prompt, user_data)
                    
                    # Calculate response time
                    response_time_ms = int((time.time() - start_time) * 1000)
                    
                    # Track assistant response
                    assistant_name = "direct_response" if enhanced_prompt and not assistant_func else \
                                   (assistant_func.__name__ if assistant_func and hasattr(assistant_func, "__name__") \
                                    else (action if action else "unknown"))
                    track_assistant_response(user_id, prompt, assistant_name, response_time_ms, 0)  # Use 0 as default tab_id
                    
                    # Display processed content
                    st.markdown(processed_content)
                    
                    # Add expandable reference section if references exist
                    if "**References Used:**" in content:
                        with st.expander("📚 View References & Assistant Details"):
                            ref_start = content.find("**References Used:**")
                            if ref_start != -1:
                                references = content[ref_start:]
                                st.markdown(references)
                                st.markdown(f"**Assistant Used:** {action.title()} Mode")
                    
                    # Add timestamp to message for persistence
                    message_with_timestamp = {
                        "role": "assistant", 
                        "content": processed_content,
                        "timestamp": int(time.time())
                    }
                    st.session_state.messages.append(message_with_timestamp)
                    
                    # Save conversation to persistent storage
                    user_id = st.session_state.get('user_id', 'anonymous')
                    save_user_conversation(user_id)
                    
                    # Show user insights in sidebar
                    if user_id != 'anonymous':
                        with st.sidebar:
                            with st.expander("👤 User Insights", expanded=False):
                                insights = get_user_insights(user_id)
                                st.json(insights)
                    
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.markdown(error_msg)
                    
                    # Add error message with timestamp
                    error_message = {
                        "role": "assistant", 
                        "content": error_msg,
                        "timestamp": int(time.time()),
                        "error": True
                    }
                    st.session_state.messages.append(error_message)
                    
                    # Save conversation with error to persistent storage
                    save_user_conversation(user_id)
                    
                    # Track error
                    track_error(user_id, prompt, str(e), 0)  # Use 0 as default tab_id