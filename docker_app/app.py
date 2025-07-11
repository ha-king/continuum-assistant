import streamlit as st
import os
from strands import Agent
from strands_tools import file_read, file_write, editor, use_llm, memory, mem0_memory
from auto_learning_system import initialize_auto_learning, trigger_manual_learning
from enhanced_learning_system import initialize_enhanced_learning, trigger_enhanced_learning
from personalized_intelligence import get_personalized_response, get_user_insights
from proactive_intelligence import initialize_proactive_intelligence, get_proactive_alerts, get_intelligence_brief, trigger_market_analysis
from ensemble_ai_system import get_ensemble_response, get_fine_tuned_response
from real_time_data_feeds import get_crypto_market_data, get_stock_market_data, get_market_sentiment, get_economic_data
from global_intelligence_system import get_global_market_status, get_timezone_intelligence, get_cultural_adaptation, predict_user_needs
from multimodal_processor import create_multimodal_interface, process_uploaded_image, analyze_financial_chart
from knowledge_graph_system import process_text_for_knowledge_graph, find_entity_connections, get_entity_network, analyze_knowledge_patterns, get_related_suggestions
from document_generator import generate_crypto_report_pdf, generate_crypto_report_pptx, create_custom_report_pdf, create_custom_report_pptx
from enhanced_pdf_generator import create_enhanced_pdf_report
from business_plan_generator import create_business_plan_interface
import asyncio
from datetime import datetime
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
from predictive_analysis_assistant import predictive_analysis_assistant
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
   - If query involves forecasting, predictive modeling, or statistical analysis → Predictive Analysis Assistant
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
        
        # Set unused assistants to False in advanced mode
        use_language = use_lafayette_economic = use_general = use_psychology = False
        use_cryptography = use_tokenomics = use_cybersec_offense = use_web3 = False
        use_formula1 = use_microchip = use_opensource = use_nuclear = False
        use_louisiana_vc = use_data_acquisition = use_automotive = False
        use_professional_networking = False
    else:
        # All assistants enabled in auto-route mode
        use_math = use_english = use_language = use_cs = use_financial = use_aws = True
        use_business_dev = use_lafayette_economic = use_research = use_louisiana_legal = True
        use_web_browser = use_general = use_psychology = use_cryptography = True
        use_blockchain = use_cryptocurrency = use_tokenomics = use_economics = True
        use_cybersec_offense = use_cybersec_defense = use_web3 = use_entrepreneurship = True
        use_formula1 = use_ai = use_microchip = use_opensource = use_nuclear = True
        use_louisiana_vc = use_data_acquisition = use_data_analysis = use_automotive = True
        use_business_contact = use_public_records = use_professional_networking = True
        use_company_intelligence = use_geopolitical = use_international_finance = True
        use_predictive_analysis = True
    
    st.divider()
    active_count = sum([use_math, use_english, use_language, use_cs, use_financial, use_aws, use_business_dev, use_lafayette_economic, use_research, use_louisiana_legal, use_web_browser, use_general, use_psychology, use_cryptography, use_blockchain, use_cryptocurrency, use_tokenomics, use_economics, use_cybersec_offense, use_cybersec_defense, use_web3, use_entrepreneurship, use_formula1, use_ai, use_microchip, use_opensource, use_nuclear, use_louisiana_vc, use_data_acquisition, use_data_analysis, use_automotive, use_business_contact, use_public_records, use_professional_networking, use_company_intelligence, use_geopolitical, use_international_finance, use_predictive_analysis])
    st.caption(f"🤖 {active_count} Assistants | 🧠 Enhanced AI | 📊 Real-time Data")
    
    # Advanced Intelligence (compact)
    with st.expander("🧠 Advanced Intelligence", expanded=False):
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        
        with adv_col1:
            if st.button("🧠 Learning", help="Trigger enhanced learning"):
                result = trigger_enhanced_learning("cryptocurrency_assistant")
                st.success("Learning triggered")
            
            if st.button("📝 Brief", help="Intelligence brief"):
                brief = get_intelligence_brief()
                st.info(brief[:100] + "...")
        
        with adv_col2:
            user_tz = st.session_state.get('user_timezone', 'UTC')
            if st.button("⏰ Timezone", help="Timezone intelligence"):
                tz_intel = get_timezone_intelligence(user_tz)
                st.info(tz_intel[:100] + "...")
            
            region = st.selectbox("Region:", ['US', 'UK', 'JP', 'DE', 'CN'], key="region_sel")
            if st.button("🌏 Culture", help="Cultural adaptation"):
                cultural_info = get_cultural_adaptation(region)
                st.info(cultural_info[:100] + "...")
        
        with adv_col3:
            if st.button("📊 Patterns", help="Knowledge patterns"):
                patterns = analyze_knowledge_patterns()
                st.info(patterns[:100] + "...")
            
            entity1 = st.text_input("Entity 1:", placeholder="Bitcoin", key="ent1")
            entity2 = st.text_input("Entity 2:", placeholder="Ethereum", key="ent2")
            if st.button("🔗 Connect") and entity1 and entity2:
                connections = find_entity_connections(entity1, entity2)
                st.info(connections[:100] + "...")


st.info("🔐 **AI-Powered Business Intelligence Platform** - Ask questions, generate reports, create business plans, and access real-time market data.")

# Quick Intelligence Panel
with st.container():
    intel_col1, intel_col2, intel_col3 = st.columns(3)
    
    with intel_col1:
        if st.button("💰 Live Crypto", help="Real-time crypto prices"):
            try:
                crypto_data = asyncio.run(get_crypto_market_data(['bitcoin', 'ethereum', 'apecoin']))
                st.success(crypto_data[:150] + "...")
            except:
                st.warning("Data unavailable")
    
    with intel_col2:
        if st.button("🌍 Markets", help="Global market status"):
            market_status = get_global_market_status()
            st.info(market_status[:150] + "...")
    
    with intel_col3:
        if st.button("🚨 Alerts", help="Intelligence alerts"):
            alerts = get_proactive_alerts()
            if alerts:
                st.warning(f"{alerts[-1]['message'][:80]}...")
            else:
                st.success("All clear")

st.divider()

# Consolidated Professional Tools
with st.expander("📄 Professional Tools Suite", expanded=False):
    tool_tab1, tool_tab2, tool_tab3 = st.tabs(["🚀 Business Plans", "📊 Reports", "📎 Media"])
    
    with tool_tab1:
        create_business_plan_interface()
    
    with tool_tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Crypto Analysis:**")
            timeframe = st.selectbox("Timeframe:", ["24h", "48h", "72h", "1w"], key="crypto_tf")
            if st.button("📊 Generate Crypto Report"):
                with st.spinner("Generating..."):
                    try:
                        pdf_data, _ = asyncio.run(generate_crypto_report_pdf(timeframe))
                        if pdf_data:
                            user_id = st.session_state.get('user_id', 'user')
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                            filename = f"crypto_analysis_{timeframe}_{user_id}_{timestamp}.pdf"
                            
                            st.download_button(
                                "Download PDF", pdf_data, filename, "application/pdf"
                            )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col2:
            st.write("**Custom Reports:**")
            custom_prompt = st.text_area("Report Topic:", height=68, placeholder="Market analysis, business strategy, etc.")
            if st.button("📝 Generate Report") and custom_prompt:
                with st.spinner("Creating..."):
                    try:
                        from strands import Agent
                        from datetime import datetime
                        
                        # Get real-time data based on topic
                        context_data = ""
                        prompt_lower = custom_prompt.lower()
                        
                        # Crypto data integration
                        if any(word in prompt_lower for word in ['crypto', 'bitcoin', 'ethereum', 'apecoin', 'price', 'market']):
                            try:
                                crypto_data = asyncio.run(get_crypto_market_data(['bitcoin', 'ethereum', 'apecoin']))
                                context_data += f"\n\nReal-time Crypto Data:\n{crypto_data}"
                            except:
                                context_data += "\n\nNote: Crypto data temporarily unavailable."
                        
                        # Market status integration
                        if any(word in prompt_lower for word in ['market', 'trading', 'stock', 'finance', 'economic']):
                            try:
                                market_status = get_global_market_status()
                                context_data += f"\n\nGlobal Market Status:\n{market_status}"
                            except:
                                context_data += "\n\nNote: Market status data temporarily unavailable."
                        
                        # Economic indicators
                        if any(word in prompt_lower for word in ['economic', 'economy', 'indicators', 'inflation', 'gdp']):
                            try:
                                economic_data = asyncio.run(get_economic_data())
                                context_data += f"\n\nEconomic Indicators:\n{economic_data}"
                            except:
                                context_data += "\n\nNote: Economic data temporarily unavailable."
                        
                        # Timezone intelligence for global topics
                        if any(word in prompt_lower for word in ['global', 'international', 'worldwide', 'timezone']):
                            try:
                                user_tz = st.session_state.get('user_timezone', 'UTC')
                                tz_intel = get_timezone_intelligence(user_tz)
                                context_data += f"\n\nTimezone Intelligence:\n{tz_intel}"
                            except:
                                pass
                        
                        # Create agent for report generation
                        agent = Agent()
                        full_prompt = f"Create a professional report on: {custom_prompt}. Current date: {datetime.now().strftime('%Y-%m-%d')}{context_data}"
                        content = str(agent(full_prompt))
                        pdf_data = create_enhanced_pdf_report(content, "Custom Report")
                        if pdf_data:
                            # Generate specific filename
                            topic_words = custom_prompt.split()[:3]  # First 3 words
                            topic_name = '_'.join(word.lower().strip('.,!?') for word in topic_words)
                            user_id = st.session_state.get('user_id', 'user')
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                            filename = f"{topic_name}_{user_id}_{timestamp}.pdf"
                            
                            st.download_button(
                                "Download PDF", pdf_data, filename, "application/pdf"
                            )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with tool_tab3:
        create_multimodal_interface()

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
if use_predictive_analysis:
    teacher_tools.append(predictive_analysis_assistant)

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
- Predictive Analysis Assistant: For forecasting, predictive modeling, and statistical analysis with best practices
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
                        # Handle crypto price queries - route to cryptocurrency assistant
                        elif any(word in prompt.lower() for word in ['crypto', 'bitcoin', 'ethereum', 'apecoin', 'price', 'coinbase']):
                            content = cryptocurrency_assistant(f"{datetime_context}{prompt}")
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
                            response = safe_execute_function(teacher_agent, full_prompt)
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
                    
                    # Process for knowledge graph
                    try:
                        kg_result = process_text_for_knowledge_graph(f"{prompt} {content}")
                        print(f"Knowledge graph: {kg_result}")
                    except:
                        pass
                    
                    # Apply ensemble AI if enabled
                    try:
                        if len(content) > 100:  # Only for substantial responses
                            enhanced_content = get_fine_tuned_response(prompt, content)
                            content = enhanced_content
                    except:
                        pass
                    
                    # Apply personalization
                    personalized_content = get_personalized_response(user_id, prompt, content)
                    
                    # Add related suggestions
                    try:
                        suggestions = get_related_suggestions(prompt)
                        if "Related Query Suggestions" in suggestions:
                            personalized_content += f"\n\n{suggestions}"
                    except:
                        pass
                    
                    # Display personalized content
                    st.markdown(personalized_content)
                    
                    # Compact document generation for substantial responses
                    if len(personalized_content) > 200:
                        doc_col1, doc_col2 = st.columns([3, 1])
                        with doc_col1:
                            doc_title = st.text_input("📄", value=f"Report_{datetime.now().strftime('%m%d')}", 
                                                    placeholder="Document title", 
                                                    key=f"doc_{tab_id}_{len(st.session_state.tab_messages[tab_id])}")
                        with doc_col2:
                            if st.button("📄 PDF", key=f"pdf_{tab_id}_{len(st.session_state.tab_messages[tab_id])}", help="Generate PDF"):
                                try:
                                    from document_generator import create_custom_report_pdf
                                    pdf_data = create_enhanced_pdf_report(personalized_content, doc_title)
                                    if pdf_data:
                                        # Generate specific filename from conversation context
                                        user_id = st.session_state.get('user_id', 'user')
                                        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                                        
                                        # Extract topic from recent messages
                                        recent_msgs = st.session_state.tab_messages[tab_id][-3:]
                                        topic_words = []
                                        for msg in recent_msgs:
                                            if msg['role'] == 'user':
                                                words = msg['content'].split()[:2]
                                                topic_words.extend(words)
                                        
                                        if topic_words:
                                            topic_name = '_'.join(word.lower().strip('.,!?') for word in topic_words[:3])
                                        else:
                                            topic_name = doc_title.lower().replace(' ', '_')
                                        
                                        filename = f"{topic_name}_{user_id}_{timestamp}.pdf"
                                        
                                        st.download_button(
                                            "⬇️", pdf_data, filename, "application/pdf",
                                            key=f"dl_{tab_id}_{len(st.session_state.tab_messages[tab_id])}"
                                        )
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                    
                    # Add expandable reference section if references exist
                    if "**References Used:**" in content:
                        with st.expander("📚 View References & Assistant Details"):
                            ref_start = content.find("**References Used:**")
                            if ref_start != -1:
                                references = content[ref_start:]
                                st.markdown(references)
                                st.markdown(f"**Assistant Used:** {action.title()} Mode")
                    
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": personalized_content})
                    
                    # Compact user insights in sidebar
                    if user_id != 'anonymous' and len(st.session_state.tab_messages[tab_id]) > 3:
                        with st.sidebar:
                            with st.expander("👤 Insights", expanded=False):
                                insights = get_user_insights(user_id)
                                st.caption(f"Level: {insights.get('expertise_level', 'N/A')} | Queries: {insights.get('interaction_count', 0)}")
                                if insights.get('primary_interest') != 'general':
                                    st.caption(f"Focus: {insights.get('primary_interest', 'N/A')}")
                    
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": error_msg})