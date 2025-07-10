import streamlit as st
import os
from strands import Agent
from strands_tools import file_read, file_write, editor, use_llm, memory, mem0_memory
from english_assistant import english_assistant
from language_assistant import language_assistant
from math_assistant import math_assistant
from computer_science_assistant import computer_science_assistant
from financial_assistant import financial_assistant
from aws_assistant import aws_assistant
from business_dev_assistant import business_dev_assistant
from lafayette_economic_assistant import lafayette_economic_assistant
from research_assistant import research_assistant
from louisiana_legal_assistant import louisiana_legal_assistant
from web_browser_assistant import web_browser_assistant
from no_expertise import general_assistant
from psychology_assistant import psychology_assistant
from cryptography_assistant import cryptography_assistant
from blockchain_assistant import blockchain_assistant
from cryptocurrency_assistant import cryptocurrency_assistant
from tokenomics_assistant import tokenomics_assistant
from economics_assistant import economics_assistant
from cybersecurity_offense_assistant import cybersecurity_offense_assistant
from cybersecurity_defense_assistant import cybersecurity_defense_assistant
from web3_assistant import web3_assistant
from entrepreneurship_assistant import entrepreneurship_assistant
from formula1_assistant import formula1_assistant
from ai_assistant import ai_assistant
from microchip_supply_chain_assistant import microchip_supply_chain_assistant
from opensource_supply_chain_assistant import opensource_supply_chain_assistant
from nuclear_energy_assistant import nuclear_energy_assistant
from louisiana_vc_assistant import louisiana_vc_assistant
from data_acquisition_assistant import data_acquisition_assistant
from data_analysis_assistant import data_analysis_assistant
from automotive_assistant import automotive_assistant
from business_contact_assistant import business_contact_assistant
from public_records_assistant import public_records_assistant
from professional_networking_assistant import professional_networking_assistant
from company_intelligence_assistant import company_intelligence_assistant
from geopolitical_assistant import geopolitical_assistant
from international_finance_assistant import international_finance_assistant
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
    
    user_tz = st.session_state.get('user_timezone', 'UTC')
    try:
        tz = pytz.timezone(user_tz)
        user_time = datetime.now(tz)
        return user_time.strftime("%A, %B %d, %Y at %I:%M %p %Z")
    except:
        return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p UTC")

def get_user_context():
    """Get user context including location and timezone"""
    context = f"Current date and time: {get_current_datetime()}\n"
    
    location = st.session_state.get('user_location')
    if location:
        context += f"User location: Latitude {location['latitude']:.4f}, Longitude {location['longitude']:.4f}\n"
    
    return context + "\n"

TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, a sophisticated educational orchestrator with ACTIVE WEB BROWSING CAPABILITIES. 
You have access to current date and time information which you must provide to all specialized agents.
Your role is to:

1. Analyze incoming student queries and determine the most appropriate specialized agent to handle them:

   AVAILABLE ASSISTANTS (ALL FUNCTIONAL):
   - Math Assistant: For mathematical calculations, problems, and concepts
   - English Assistant: For writing, grammar, literature, and composition
   - Language Assistant: For translation and language-related queries
   - Computer Science Assistant: For programming, algorithms, data structures, and code execution
   - Financial Assistant: For financial records, reports, accounting, and business finance
   - AWS Assistant: For cloud architecture, AWS services, and best practices
   - Business Dev Assistant: For business development, partnerships, and growth strategies
   - Lafayette Economic Assistant: For economic opportunities in Lafayette, Louisiana
   - Research Assistant: *** ACTIVE AND FUNCTIONAL *** For internet research and web-based information gathering with real-time data access
   - Louisiana Legal Assistant: For Louisiana business legal matters and compliance
   - Web Browser Assistant: *** ACTIVE AND FUNCTIONAL *** For real-time website browsing, content analysis, company research, and any website-related queries
   - General Assistant: For all other topics outside these specialized domains
   - Automotive Assistant: For auto mechanics, repair diagnosis, suspension systems, steering alignment, electrical diagrams, and electronics

   IMPORTANT: The Web Browser Assistant IS AVAILABLE AND FUNCTIONAL - use it for ANY website-related queries.

2. Key Responsibilities:
   - Accurately classify student queries by subject area
   - Route requests to the appropriate specialized agent
   - Maintain context and coordinate multi-step problems
   - Ensure cohesive responses when multiple agents are needed

3. Decision Protocol:
   - If query involves calculations/numbers → Math Assistant
   - If query involves writing/literature/grammar → English Assistant
   - If query involves translation → Language Assistant
   - If query involves programming/coding/algorithms/computer science → Computer Science Assistant
   - If query involves finance/accounting/business reports → Financial Assistant
   - If query involves AWS/cloud architecture/best practices → AWS Assistant
   - If query involves business development/partnerships/growth → Business Dev Assistant
   - If query involves Lafayette LA economic opportunities → Lafayette Economic Assistant
   - If query involves research/web search/current information/real-time data → Research Assistant
   - If query involves Louisiana legal/business law matters → Louisiana Legal Assistant
   - If query involves browsing websites/viewing web content/website analysis/company information → Web Browser Assistant
   - If query mentions specific websites (like .com, .org) or asks to "browse" or "visit" → Web Browser Assistant
   - If query asks about company offerings, services, or business analysis → Web Browser Assistant
   - If query involves automotive repair, mechanics, car diagnostics, suspension, alignment, or car electronics → Automotive Assistant
   - If query involves business contact research or company contact information → Business Contact Assistant
   - If query involves public records research or legal compliance → Public Records Assistant
   - If query involves professional networking or business development → Professional Networking Assistant
   - If query involves competitive analysis or company intelligence → Company Intelligence Assistant
   - If query involves geopolitical analysis or international relations → Geopolitical Assistant
   - If query involves international finance or global monetary systems → International Finance Assistant
   - If query is outside these specialized areas → General Assistant
   - For complex queries, coordinate multiple agents as needed

*** MANDATORY WEB BROWSING RULES - NO EXCEPTIONS ***:
- ANY query containing "browse", "website", "visit", ".com", ".org", "infascination", "company", "current", "today", "now", "latest" → IMMEDIATELY use web_browser_assistant or research_assistant tool
- ANY query asking about specific companies or their information → IMMEDIATELY use web_browser_assistant tool
- ANY query requesting website analysis or company research → IMMEDIATELY use web_browser_assistant tool
- If user asks to browse ANY website → CALL web_browser_assistant(query) IMMEDIATELY
- If user mentions ANY company name → CALL web_browser_assistant(query) IMMEDIATELY

*** CRITICAL: You HAVE web browsing capabilities through the web_browser_assistant tool. NEVER claim you don't have web browsing capabilities. ***

*** MANDATORY ROUTING CHECK ***:
1. Does the query mention websites, companies, browsing, or .com/.org domains? → YES = CALL web_browser_assistant(query)
2. Does the query ask about company information or services? → YES = CALL web_browser_assistant(query)
3. Does the query request website analysis? → YES = CALL web_browser_assistant(query)

IF ANY OF THE ABOVE = YES, YOU MUST USE THE WEB BROWSER ASSISTANT TOOL.

Always confirm your understanding before routing to ensure accurate assistance.
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
    
    st.subheader("Teacher Agents")
    use_math = st.checkbox("Math Assistant", value=True)
    use_english = st.checkbox("English Assistant", value=True)
    use_language = st.checkbox("Language Assistant", value=True)
    use_cs = st.checkbox("Computer Science Assistant", value=True)
    use_financial = st.checkbox("Financial Assistant", value=True)
    use_aws = st.checkbox("AWS Assistant", value=True)
    use_business_dev = st.checkbox("Business Dev Assistant", value=True)
    use_lafayette_economic = st.checkbox("Lafayette Economic Assistant", value=True)
    use_research = st.checkbox("Research Assistant", value=True)
    use_louisiana_legal = st.checkbox("Louisiana Legal Assistant", value=True)
    use_web_browser = st.checkbox("Web Browser Assistant", value=True)
    use_general = st.checkbox("General Assistant", value=True)
    
    st.subheader("Specialized Experts")
    use_psychology = st.checkbox("Psychology Assistant", value=True)
    use_cryptography = st.checkbox("Cryptography Assistant", value=True)
    use_blockchain = st.checkbox("Blockchain Assistant", value=True)
    use_cryptocurrency = st.checkbox("Cryptocurrency Assistant", value=True)
    use_tokenomics = st.checkbox("Tokenomics Assistant", value=True)
    use_economics = st.checkbox("Economics Assistant", value=True)
    use_cybersec_offense = st.checkbox("Cybersecurity Offense Assistant", value=True)
    use_cybersec_defense = st.checkbox("Cybersecurity Defense Assistant", value=True)
    use_web3 = st.checkbox("Web3 Assistant", value=True)
    use_entrepreneurship = st.checkbox("Entrepreneurship Assistant", value=True)
    use_formula1 = st.checkbox("Formula 1 Assistant", value=True)
    use_ai = st.checkbox("AI Assistant", value=True)
    use_microchip = st.checkbox("Microchip Supply Chain Assistant", value=True)
    use_opensource = st.checkbox("Open Source Supply Chain Assistant", value=True)
    use_nuclear = st.checkbox("Nuclear Energy Assistant", value=True)
    use_louisiana_vc = st.checkbox("Louisiana VC Assistant", value=True)
    use_data_acquisition = st.checkbox("Data Acquisition Assistant", value=True)
    use_data_analysis = st.checkbox("Data Analysis Assistant", value=True)
    use_automotive = st.checkbox("Automotive Assistant", value=True)
    
    st.subheader("Business Research")
    use_business_contact = st.checkbox("Business Contact Assistant", value=True)
    use_public_records = st.checkbox("Public Records Assistant", value=True)
    use_professional_networking = st.checkbox("Professional Networking Assistant", value=True)
    use_company_intelligence = st.checkbox("Company Intelligence Assistant", value=True)
    
    st.subheader("Global Analysis")
    use_geopolitical = st.checkbox("Geopolitical Assistant", value=True)
    use_international_finance = st.checkbox("International Finance Assistant", value=True)
    
    st.divider()
    if st.button("🛑 Stop Session", type="primary"):
        st.stop()

st.write("🔐 **Authenticated Access** - Ask a question in any subject area, and I'll route it to the appropriate specialist.")

teacher_tools = []
if use_math:
    teacher_tools.append(math_assistant)
if use_language:
    teacher_tools.append(language_assistant)
if use_english:
    teacher_tools.append(english_assistant)
if use_cs:
    teacher_tools.append(computer_science_assistant)
if use_financial:
    teacher_tools.append(financial_assistant)
if use_aws:
    teacher_tools.append(aws_assistant)
if use_business_dev:
    teacher_tools.append(business_dev_assistant)
if use_lafayette_economic:
    teacher_tools.append(lafayette_economic_assistant)
if use_research:
    teacher_tools.append(research_assistant)
if use_louisiana_legal:
    teacher_tools.append(louisiana_legal_assistant)
if use_web_browser:
    teacher_tools.append(web_browser_assistant)
if use_general:
    teacher_tools.append(general_assistant)
if use_psychology:
    teacher_tools.append(psychology_assistant)
if use_cryptography:
    teacher_tools.append(cryptography_assistant)
if use_blockchain:
    teacher_tools.append(blockchain_assistant)
if use_cryptocurrency:
    teacher_tools.append(cryptocurrency_assistant)
if use_tokenomics:
    teacher_tools.append(tokenomics_assistant)
if use_economics:
    teacher_tools.append(economics_assistant)
if use_cybersec_offense:
    teacher_tools.append(cybersecurity_offense_assistant)
if use_cybersec_defense:
    teacher_tools.append(cybersecurity_defense_assistant)
if use_web3:
    teacher_tools.append(web3_assistant)
if use_entrepreneurship:
    teacher_tools.append(entrepreneurship_assistant)
if use_formula1:
    teacher_tools.append(formula1_assistant)
if use_ai:
    teacher_tools.append(ai_assistant)
if use_microchip:
    teacher_tools.append(microchip_supply_chain_assistant)
if use_opensource:
    teacher_tools.append(opensource_supply_chain_assistant)
if use_nuclear:
    teacher_tools.append(nuclear_energy_assistant)
if use_louisiana_vc:
    teacher_tools.append(louisiana_vc_assistant)
if use_data_acquisition:
    teacher_tools.append(data_acquisition_assistant)
if use_data_analysis:
    teacher_tools.append(data_analysis_assistant)
if use_automotive:
    teacher_tools.append(automotive_assistant)
if use_business_contact:
    teacher_tools.append(business_contact_assistant)
if use_public_records:
    teacher_tools.append(public_records_assistant)
if use_professional_networking:
    teacher_tools.append(professional_networking_assistant)
if use_company_intelligence:
    teacher_tools.append(company_intelligence_assistant)
if use_geopolitical:
    teacher_tools.append(geopolitical_assistant)
if use_international_finance:
    teacher_tools.append(international_finance_assistant)

# Create teacher agent with datetime awareness
def create_teacher_agent_with_datetime():
    user_context = get_user_context()
    enhanced_prompt = f"""{TEACHER_SYSTEM_PROMPT}

*** CRITICAL CONTEXT INSTRUCTION ***:
{user_context}
You MUST include this current date/time and location information when calling ANY specialized agent tool.
When routing queries to specialized agents, always prepend the user context to ensure they have temporal and geographical awareness.

*** TIME/DATE QUERIES ***:
If user asks "what time is it", "what day is it", "current time", "current date", or similar:
Respond directly with: "It is {user_context.strip()}" - DO NOT route to other agents.

AVAILABLE ASSISTANTS (Updated):
- Automotive Assistant: For auto mechanics, repair diagnosis, suspension systems, steering alignment, electrical diagrams, and electronics
- Business Contact Assistant: For finding legitimate business contact information and company contacts
- Public Records Assistant: For public records research and legal compliance guidance
- Professional Networking Assistant: For business networking and professional relationship building
- Company Intelligence Assistant: For competitive analysis and business intelligence research
- Geopolitical Assistant: For geopolitical analysis and international relations expertise
- International Finance Assistant: For global finance and international monetary systems analysis
"""
    return Agent(
        system_prompt=enhanced_prompt,
        callback_handler=None,
        tools=teacher_tools
    )

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
                    
                    # Display main content
                    st.markdown(content)
                    
                    # Add expandable reference section if references exist
                    if "**References Used:**" in content:
                        with st.expander("📚 View References & Assistant Details"):
                            ref_start = content.find("**References Used:**")
                            if ref_start != -1:
                                references = content[ref_start:]
                                st.markdown(references)
                                st.markdown(f"**Assistant Used:** {action.title()} Mode")
                    
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": content})
                    
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": error_msg})