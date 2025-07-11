import boto3
import json
import base64
import io
from PIL import Image
import streamlit as st

class MultiModalProcessor:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.textract = boto3.client('textract', region_name='us-west-2')
        self.polly = boto3.client('polly', region_name='us-west-2')
        self.transcribe = boto3.client('transcribe', region_name='us-west-2')
        
    def process_image(self, image_data, query="Analyze this image"):
        """Process image with AI vision"""
        try:
            # Convert image to base64
            if isinstance(image_data, bytes):
                image_b64 = base64.b64encode(image_data).decode()
            else:
                # Handle PIL Image
                buffer = io.BytesIO()
                image_data.save(buffer, format='PNG')
                image_b64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Use Claude 3 for image analysis
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v1:0",
                body=json.dumps({
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": query},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_b64
                                }
                            }
                        ]
                    }],
                    "max_tokens": 500,
                    "temperature": 0.3
                })
            )
            
            result = json.loads(response['body'].read())
            return result.get('content', [{}])[0].get('text', 'Unable to analyze image')
            
        except Exception as e:
            return f"Image processing error: {str(e)}"
    
    def extract_text_from_pdf(self, pdf_bytes):
        """Extract text from PDF using Textract"""
        try:
            response = self.textract.detect_document_text(
                Document={'Bytes': pdf_bytes}
            )
            
            text_blocks = []
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    text_blocks.append(block['Text'])
            
            extracted_text = '\n'.join(text_blocks)
            return f"📄 **Extracted Text:**\n\n{extracted_text}"
            
        except Exception as e:
            return f"PDF processing error: {str(e)}"
    
    def analyze_chart_or_graph(self, image_data):
        """Specialized analysis for charts and graphs"""
        analysis_prompt = """
        Analyze this chart/graph and provide:
        1. Type of chart (bar, line, pie, etc.)
        2. Key data points and trends
        3. Main insights and conclusions
        4. Any notable patterns or anomalies
        
        Be specific with numbers and percentages where visible.
        """
        
        return self.process_image(image_data, analysis_prompt)
    
    def text_to_speech(self, text, voice_id='Joanna'):
        """Convert text to speech using Polly"""
        try:
            # Limit text length for demo
            if len(text) > 1000:
                text = text[:1000] + "..."
            
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine='neural'
            )
            
            # Return audio stream
            return response['AudioStream'].read()
            
        except Exception as e:
            return f"Text-to-speech error: {str(e)}"
    
    def analyze_document_structure(self, image_data):
        """Analyze document structure and layout"""
        structure_prompt = """
        Analyze this document and describe:
        1. Document type (report, invoice, form, etc.)
        2. Layout structure and sections
        3. Key information fields
        4. Data extraction opportunities
        5. Quality and readability assessment
        """
        
        return self.process_image(image_data, structure_prompt)
    
    def process_financial_chart(self, image_data):
        """Specialized processing for financial charts"""
        financial_prompt = """
        Analyze this financial chart/graph:
        1. Identify the financial instrument or metric
        2. Time period covered
        3. Price/value trends and patterns
        4. Support and resistance levels
        5. Technical indicators if visible
        6. Investment insights and recommendations
        
        Provide specific numerical analysis where possible.
        """
        
        return self.process_image(image_data, financial_prompt)
    
    def create_voice_interface(self):
        """Create voice interface components"""
        st.subheader("🎤 Voice Interface")
        
        # Voice input placeholder
        if st.button("🎙️ Start Voice Input"):
            st.info("Voice input would be processed here (requires additional setup)")
        
        # Text-to-speech demo
        text_input = st.text_area("Enter text for speech synthesis:", 
                                 value="Hello, this is your AI assistant speaking.")
        
        voice_options = ['Joanna', 'Matthew', 'Amy', 'Brian', 'Emma']
        selected_voice = st.selectbox("Select Voice:", voice_options)
        
        if st.button("🔊 Generate Speech"):
            try:
                audio_data = self.text_to_speech(text_input, selected_voice)
                if isinstance(audio_data, bytes):
                    st.audio(audio_data, format='audio/mp3')
                else:
                    st.error(audio_data)
            except Exception as e:
                st.error(f"Speech generation error: {str(e)}")

# Global instance
multimodal = MultiModalProcessor()

def process_uploaded_image(image_file, query="Analyze this image"):
    """Process uploaded image file"""
    try:
        image = Image.open(image_file)
        return multimodal.process_image(image, query)
    except Exception as e:
        return f"Image upload error: {str(e)}"

def process_uploaded_pdf(pdf_file):
    """Process uploaded PDF file"""
    try:
        pdf_bytes = pdf_file.read()
        return multimodal.extract_text_from_pdf(pdf_bytes)
    except Exception as e:
        return f"PDF upload error: {str(e)}"

def analyze_financial_chart(image_file):
    """Analyze financial chart from uploaded image"""
    try:
        image = Image.open(image_file)
        return multimodal.process_financial_chart(image)
    except Exception as e:
        return f"Chart analysis error: {str(e)}"

def create_multimodal_interface():
    """Create multimodal interface in Streamlit"""
    st.subheader("📎 Multi-Modal Processing")
    
    tab1, tab2, tab3 = st.tabs(["📷 Image Analysis", "📄 Document Processing", "🎤 Voice Interface"])
    
    with tab1:
        uploaded_image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            analysis_type = st.selectbox("Analysis Type:", 
                                       ["General Analysis", "Financial Chart", "Document Structure"])
            
            if st.button("Analyze Image"):
                if analysis_type == "Financial Chart":
                    result = analyze_financial_chart(uploaded_image)
                elif analysis_type == "Document Structure":
                    image = Image.open(uploaded_image)
                    result = multimodal.analyze_document_structure(image)
                else:
                    result = process_uploaded_image(uploaded_image)
                
                st.markdown(result)
    
    with tab2:
        uploaded_pdf = st.file_uploader("Upload PDF", type=['pdf'])
        if uploaded_pdf:
            if st.button("Extract Text from PDF"):
                result = process_uploaded_pdf(uploaded_pdf)
                st.markdown(result)
    
    with tab3:
        multimodal.create_voice_interface()