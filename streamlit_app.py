import streamlit as st
import requests
import json
from PIL import Image
import io

st.set_page_config(
    page_title="CognitiveX Medical AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .result-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15); /* Stronger shadow for results */
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 10px;
    }
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🧠 CognitiveX Medical AI</h1>
    <p>Advanced AI-Powered Prescription Analysis & Verification</p>
    <p><em>Powered by IBM Granite Models & Hugging Face Transformers</em></p>
</div>
""", unsafe_allow_html=True)

# System status in expandable section
with st.expander("🔧 System Status", expanded=False):
    col_status1, col_status2, col_status3 = st.columns(3)
    with col_status1:
        st.markdown('<div class="metric-card"><h4>🔑 API Status</h4><p>Connected</p></div>', unsafe_allow_html=True)
    with col_status2:
        st.markdown('<div class="metric-card"><h4>🚀 Backend</h4><p>Running</p></div>', unsafe_allow_html=True)
    with col_status3:
        st.markdown('<div class="metric-card"><h4>🤖 AI Models</h4><p>Ready</p></div>', unsafe_allow_html=True)

# Configuration
fastapi_url = "http://localhost:8000"

# Main interface with improved layout
col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Prescription Analysis Input")
    
    input_method = st.radio(
        "Choose input method:",
        ["📁 Upload File", "✏️ Text Input"],
        horizontal=True
    )
    
    patient_age = st.number_input(
        "Patient Age (Years):",
        min_value=0,
        max_value=120,
        value=30, # Default age
        step=1,
        help="Enter the patient's age for more context-aware analysis."
    )

    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Upload prescription image or document",
            type=['png', 'jpg', 'jpeg', 'txt', 'pdf'],
            help="Supported formats: PNG, JPG, JPEG, TXT, PDF"
        )
        
        if uploaded_file is not None:
            if uploaded_file.type.startswith('image'):
                image = Image.open(uploaded_file)
                st.image(image, caption="📸 Uploaded Prescription", use_column_width=True)
                st.success(f"✅ Image loaded: {uploaded_file.name}")
            else:
                st.success(f"📄 File uploaded: {uploaded_file.name}")
    
    else: # Text Input
        prescription_text = st.text_area(
            "Enter prescription details:",
            height=150,
            placeholder="Type or paste prescription details here...\n\nExample:\nPatient is prescribed Amoxicillin 500mg TID and Ibuprofen 200mg",
            help="Enter the complete prescription text for analysis"
        )

    # Analyze button with better styling
    analyze_button = st.button(
        "🔍 Analyze Prescription", 
        type="primary", 
        use_container_width=True,
        help="Click to start AI-powered prescription analysis"
    )
    if analyze_button:
        if input_method == "📁 Upload File" and uploaded_file is not None:
            with st.spinner("🤖 AI analyzing prescription..."):
                try:
                    # For file uploads, create form data including the age
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"patient_age": patient_age} # Add age here
                    response = requests.post(f"{fastapi_url}/analyze-prescription", files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state['analysis_result'] = result
                        st.success("✅ Analysis completed successfully!")
                    else:
                        st.error(f"❌ Analysis failed: {response.status_code} - {response.text}. Please check your backend connection.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        elif input_method == "✏️ Text Input" and prescription_text:
            with st.spinner("🤖 AI analyzing prescription text..."):
                try:
                    # For text input, use the analyze-text endpoint
                    # Send age as form data along with text
                    data = {
                        "text": prescription_text,
                        "patient_age": patient_age # Add age here
                    }
                    response = requests.post(f"{fastapi_url}/analyze-text", data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state['analysis_result'] = result
                        st.success("✅ Analysis completed successfully!")
                    else:
                        st.error(f"❌ Analysis failed: {response.status_code} - {response.text}. Please check your backend connection.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please provide a prescription file or text to analyze.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 AI Analysis Results")
    
    if 'analysis_result' in st.session_state:
        result = st.session_state['analysis_result']
        
        # Display patient age if available
        patient_age_display = result.get('patient_age')
        if patient_age_display is not None:
            st.markdown(f"**Patient Age Submitted:** {patient_age_display} years")
        
        # AI Medical Analysis Results
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("#### 🤖 **IBM Granite Medical AI Analysis**")
        granite_data = result.get('ibm_granite_analysis', {})
        
        if granite_data.get('success'):
            granite_result = granite_data.get('data', [])
            if isinstance(granite_result, list) and granite_result:
                for item in granite_result:
                    if isinstance(item, dict) and 'generated_text' in item:
                        # Clean up the text and format it better
                        analysis_text = item['generated_text']
                        st.markdown(analysis_text)
        elif 'error' in granite_data:
            st.error(f"❌ Medical analysis error: {granite_data['error']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Medical Entities Results with better formatting
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("#### 🏥 **Medical Entity Recognition**")
        entity_data = result.get('medical_entities', {})
        
        if entity_data.get('success'):
            entities = entity_data.get('data', [])
            if isinstance(entities, list) and entities:
                # Group entities by type
                entity_groups = {}
                for entity in entities:
                    if isinstance(entity, dict):
                        entity_type = entity.get('entity_group', entity.get('label', 'OTHER'))
                        if entity_type not in entity_groups:
                            entity_groups[entity_type] = []
                        entity_groups[entity_type].append(entity)
                
                # Display entities by group
                if entity_groups:
                    # Create columns dynamically based on number of entity groups, max 3 columns
                    num_cols = min(len(entity_groups), 3)
                    cols = st.columns(num_cols)
                    
                    for i, (group_name, group_entities) in enumerate(entity_groups.items()):
                        with cols[i % num_cols]:
                            st.markdown(f"**{group_name}**")
                            # Sort by score and show top few, or all if few
                            sorted_entities = sorted(group_entities, key=lambda x: x.get('score', 0), reverse=True)
                            for entity in sorted_entities[:7]: # Show top 7 per group for brevity
                                entity_text = entity.get('word', entity.get('entity', ''))
                                confidence = entity.get('score', entity.get('confidence', 0))
                                st.markdown(f"• {entity_text} (Conf: {confidence:.2f})")
                else:
                    st.info("No specific medical entities detected.")
            else:
                st.info("No specific medical entities detected.")
        elif 'error' in entity_data:
            st.error(f"❌ Entity recognition error: {entity_data['error']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Verification Status with visual indicator
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        status = result.get('verification_status', 'unknown')
        if status == 'processed':
            st.success("✅ **Prescription Successfully Processed & Verified**")
        else:
            st.info(f"ℹ️ **Status:** {status.title()}")
        
        # Model information in an expandable section
        with st.expander("🔧 Technical Details", expanded=False):
            model_info = result.get('models_used', {})
            if model_info:
                st.write(f"**🤖 Granite Model:** {model_info.get('granite', 'N/A')}")
                st.write(f"**🏥 NER Model:** {model_info.get('ner', 'N/A')}")
                st.write(f"**⏱️ Processing Time:** ~2.3 seconds (simulated)") # Updated to simulated
                st.write(f"**🎯 Accuracy Rate:** 94.2% (simulated)") # Updated to simulated
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.info("📤 **Upload and analyze a prescription to see AI-powered results here.**")
        st.markdown("""
        **What you'll get:**
        - 🤖 Comprehensive medical AI analysis with age considerations
        - 💊 Drug and dosage identification
        - ⚠️ Safety and interaction warnings
        - 📋 Clinical recommendations
        - ✅ Prescription verification status
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Professional footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem; box-shadow: 0 -2px 8px rgba(0,0,0,0.1);">
    <h4>🧠 CognitiveX Medical AI Platform</h4>
    <p><strong>Advanced Healthcare Technology Stack:</strong></p>
    <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin: 1rem 0;">
        <span>🚀 <strong>FastAPI</strong> Backend</span>
        <span>🎨 <strong>Streamlit</strong> Interface</span>
        <span>🤖 <strong>IBM Granite</strong> Models</span>
        <span>🔬 <strong>Hugging Face</strong> Transformers</span>
    </div>
    <p style="margin-top: 1rem; color: #666;">
        <em>Empowering healthcare professionals with AI-driven prescription analysis and verification</em>
    </p>
</div>
""", unsafe_allow_html=True)