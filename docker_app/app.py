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
from utils.auth import Auth
from config_file import Config

# Authentication setup
try:
    authenticator = Auth.get_authenticator(
        secret_id=Config.SECRETS_MANAGER_ID,
        region=Config.DEPLOYMENT_REGION
    )
    
    # Check authentication
    is_logged_in = authenticator.login()
    
    if not is_logged_in:
        st.stop()
        
except Exception as e:
    st.error(f"Authentication error: {str(e)}")
    st.stop()

TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, a sophisticated educational orchestrator with ACTIVE WEB BROWSING CAPABILITIES. Your role is to:

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
   - Research Assistant: For internet research and web-based information gathering
   - Louisiana Legal Assistant: For Louisiana business legal matters and compliance
   - Web Browser Assistant: *** ACTIVE AND FUNCTIONAL *** For real-time website browsing, content analysis, company research, and any website-related queries
   - General Assistant: For all other topics outside these specialized domains

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
   - If query involves research/web search/current information → Research Assistant
   - If query involves Louisiana legal/business law matters → Louisiana Legal Assistant
   - If query involves browsing websites/viewing web content/website analysis/company information → Web Browser Assistant
   - If query mentions specific websites (like .com, .org) or asks to "browse" or "visit" → Web Browser Assistant
   - If query asks about company offerings, services, or business analysis → Web Browser Assistant
   - If query is outside these specialized areas → General Assistant
   - For complex queries, coordinate multiple agents as needed

*** MANDATORY WEB BROWSING RULES - NO EXCEPTIONS ***:
- ANY query containing "browse", "website", "visit", ".com", ".org", "infascination", "company" → IMMEDIATELY use web_browser_assistant tool
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

def run_kb_agent(query):
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
                prompt=f"User question: \"{query}\"\n\nInformation: {str(result)}\n\nProvide a helpful answer:",
                system_prompt="You are a helpful knowledge assistant that provides clear, concise answers based on information retrieved from a knowledge base."
            )
            return str(answer)
    except Exception:
        return "Knowledge base is not configured. Please use the teacher mode for educational questions."

def run_memory_agent(query):
    agent = Agent(system_prompt="You are a personal assistant that maintains context by remembering user details.", tools=[mem0_memory, use_llm])
    response = agent(query)
    return str(response)

st.title("🔒 Continuum Assistant")

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
        "anthropic.claude-3-7-sonnet-20250219-v1:0",
        "anthropic.claude-sonnet-4-20250514-v1:0"
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

teacher_agent = Agent(
    system_prompt=TEACHER_SYSTEM_PROMPT,
    callback_handler=None,
    tools=teacher_tools
)

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
                    router_agent = Agent(tools=[use_llm])
                    action = determine_action(router_agent, prompt)
                    
                    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.tab_messages[tab_id][-10:]])
                    full_prompt = f"Context: {context}\n\nCurrent question: {prompt}" if context else prompt
                    
                    if action == "teacher":
                        if any(word in prompt.lower() for word in ['browse', 'infascination', '.com', 'website', 'visit']):
                            try:
                                content = web_browser_assistant(prompt)
                            except Exception as e:
                                response = teacher_agent(full_prompt)
                                content = str(response)
                        else:
                            response = teacher_agent(full_prompt)
                            content = str(response)
                    else:
                        if memory_backend == "OpenSearch Memory":
                            content = run_memory_agent(full_prompt)
                        else:
                            kb_result = run_kb_agent(full_prompt)
                            if "Knowledge base is not configured" in kb_result:
                                response = teacher_agent(full_prompt)
                                content = str(response)
                            else:
                                content = kb_result
                    
                    st.markdown(content)
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": content})
                    
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.tab_messages[tab_id].append({"role": "assistant", "content": error_msg})