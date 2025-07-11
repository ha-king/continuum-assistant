import boto3
import json
from datetime import datetime
import streamlit as st

class BusinessPlanGenerator:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.plan_sections = [
            "Executive Summary",
            "Company Description", 
            "Market Analysis",
            "Organization & Management",
            "Products/Services",
            "Marketing & Sales Strategy",
            "Financial Projections",
            "Funding Requirements",
            "Implementation Timeline"
        ]
        
    def start_interactive_session(self):
        """Start interactive business plan generation"""
        if 'bp_stage' not in st.session_state:
            st.session_state.bp_stage = 'initial'
            st.session_state.bp_data = {}
            st.session_state.bp_questions = []
            st.session_state.bp_responses = []
        
        return self.get_next_question()
    
    def get_next_question(self):
        """Get the next question based on current stage"""
        stage = st.session_state.bp_stage
        
        questions = {
            'initial': "What is your business idea or concept? Please provide a brief description of what your business will do.",
            'industry': "What industry or market sector does your business operate in? (e.g., technology, healthcare, retail, etc.)",
            'target_market': "Who is your target customer? Describe your ideal customer demographics and characteristics.",
            'problem_solution': "What specific problem does your business solve? How is your solution unique or better than existing alternatives?",
            'business_model': "How will your business make money? Describe your revenue model (subscription, one-time sales, advertising, etc.)",
            'competition': "Who are your main competitors? What advantages do you have over them?",
            'team': "Tell me about your team. What relevant experience and skills do the founders/key team members have?",
            'funding': "How much funding do you need? What will you use the money for?",
            'timeline': "What are your key milestones for the first 12-24 months?",
            'financials': "Do you have any financial projections or revenue estimates? What are your expected costs?"
        }
        
        return questions.get(stage, "Let me generate your business plan now.")
    
    def process_response(self, user_response):
        """Process user response and determine next question"""
        stage = st.session_state.bp_stage
        
        # Store the response
        st.session_state.bp_data[stage] = user_response
        st.session_state.bp_responses.append(f"{stage}: {user_response}")
        
        # Determine next stage
        stage_flow = [
            'initial', 'industry', 'target_market', 'problem_solution', 
            'business_model', 'competition', 'team', 'funding', 
            'timeline', 'financials', 'complete'
        ]
        
        current_index = stage_flow.index(stage)
        if current_index < len(stage_flow) - 1:
            st.session_state.bp_stage = stage_flow[current_index + 1]
            return self.get_next_question()
        else:
            st.session_state.bp_stage = 'complete'
            return "Ready to generate your business plan!"
    
    def ask_clarifying_question(self, section, user_data):
        """Ask AI to generate clarifying questions for specific sections"""
        try:
            clarification_prompt = f"""
            Based on this business information: {user_data}
            
            I need to create a detailed {section} section for a business plan.
            What 2-3 specific clarifying questions should I ask to make this section comprehensive and professional?
            
            Focus on questions that would help create:
            - Specific, actionable content
            - Professional business language
            - Detailed analysis and projections
            
            Return only the questions, numbered 1-3.
            """
            
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": clarification_prompt}],
                    "max_tokens": 300,
                    "temperature": 0.3
                })
            )
            
            result = json.loads(response['body'].read())
            return result.get('content', [{}])[0].get('text', 'No clarifying questions needed.')
            
        except Exception as e:
            return f"Error generating questions: {str(e)}"
    
    def generate_business_plan_section(self, section, user_data, additional_info=""):
        """Generate a specific section of the business plan"""
        try:
            section_prompt = f"""
            Create a professional {section} section for a business plan based on this information:
            
            Business Data: {user_data}
            Additional Details: {additional_info}
            
            Requirements for {section}:
            - Professional business language
            - Specific details and metrics where possible
            - Industry-standard format and content
            - Actionable insights and strategies
            - 2-3 paragraphs minimum
            
            Current date: {datetime.now().strftime('%B %Y')}
            
            Write only the {section} content, well-formatted with clear structure.
            """
            
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": section_prompt}],
                    "max_tokens": 600,
                    "temperature": 0.2
                })
            )
            
            result = json.loads(response['body'].read())
            return result.get('content', [{}])[0].get('text', f'Error generating {section}')
            
        except Exception as e:
            return f"Error generating {section}: {str(e)}"
    
    def generate_complete_business_plan(self):
        """Generate the complete business plan"""
        if st.session_state.bp_stage != 'complete':
            return "Business plan data collection not complete."
        
        user_data = st.session_state.bp_data
        
        # Generate each section
        business_plan = f"""
# BUSINESS PLAN
## {user_data.get('initial', 'Business Concept')}

*Generated on {datetime.now().strftime('%B %d, %Y')}*

---

"""
        
        for section in self.plan_sections:
            section_content = self.generate_business_plan_section(section, user_data)
            business_plan += f"## {section}\n\n{section_content}\n\n---\n\n"
        
        # Add appendix with user responses
        business_plan += """## Appendix: Planning Session Notes

"""
        for response in st.session_state.bp_responses:
            business_plan += f"- {response}\n"
        
        return business_plan
    
    def create_interactive_interface(self):
        """Create the interactive business plan interface"""
        st.subheader("🚀 Interactive Business Plan Generator")
        
        if 'bp_stage' not in st.session_state:
            st.info("Let's create a comprehensive business plan together! I'll ask you questions to gather the information needed.")
            if st.button("Start Business Plan Creation"):
                self.start_interactive_session()
                st.rerun()
        
        elif st.session_state.bp_stage == 'complete':
            st.success("✅ All information collected! Ready to generate your business plan.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📄 Generate Business Plan"):
                    with st.spinner("Creating your comprehensive business plan..."):
                        business_plan = self.generate_complete_business_plan()
                        st.session_state.generated_bp = business_plan
                        st.success("Business plan generated!")
            
            with col2:
                if st.button("🔄 Start Over"):
                    for key in ['bp_stage', 'bp_data', 'bp_questions', 'bp_responses', 'generated_bp']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            # Display generated business plan
            if 'generated_bp' in st.session_state:
                st.markdown("### Your Business Plan:")
                st.markdown(st.session_state.generated_bp)
                
                # Document generation options
                st.markdown("### Download Options:")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📄 Download as PDF"):
                        from document_generator import create_custom_report_pdf
                        pdf_data = create_custom_report_pdf("Business Plan", st.session_state.generated_bp)
                        if pdf_data:
                            st.download_button(
                                label="📄 Download PDF",
                                data=pdf_data,
                                file_name=f"business_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf"
                            )
                
                with col2:
                    if st.button("📊 Download as PowerPoint"):
                        from document_generator import create_custom_report_pptx
                        pptx_data = create_custom_report_pptx("Business Plan", st.session_state.generated_bp)
                        if pptx_data:
                            st.download_button(
                                label="📊 Download PPTX",
                                data=pptx_data,
                                file_name=f"business_plan_{datetime.now().strftime('%Y%m%d')}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )
        
        else:
            # Show progress
            stage_flow = ['initial', 'industry', 'target_market', 'problem_solution', 'business_model', 'competition', 'team', 'funding', 'timeline', 'financials']
            current_index = stage_flow.index(st.session_state.bp_stage)
            progress = (current_index + 1) / len(stage_flow)
            
            st.progress(progress)
            st.write(f"Step {current_index + 1} of {len(stage_flow)}")
            
            # Show current question
            question = self.get_next_question()
            st.markdown(f"### {question}")
            
            # Get user response
            user_response = st.text_area("Your response:", height=100, key=f"response_{st.session_state.bp_stage}")
            
            if st.button("Next Question") and user_response:
                next_question = self.process_response(user_response)
                st.rerun()
            
            # Show collected data so far
            if st.session_state.bp_data:
                with st.expander("📋 Information Collected So Far"):
                    for stage, response in st.session_state.bp_data.items():
                        st.write(f"**{stage.replace('_', ' ').title()}:** {response}")

# Global instance
bp_generator = BusinessPlanGenerator()

def create_business_plan_interface():
    """Create business plan generator interface"""
    return bp_generator.create_interactive_interface()