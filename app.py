# ai_medical_checker/app.py

import streamlit as st
import requests
import base64

# This is the Streamlit frontend. It is responsible for the UI
# and making requests to the FastAPI backend.

def main():
    """
    Streamlit UI for the application.
    """
    # Set up the page configuration with a title
    st.set_page_config(page_title="AI Medical Prescription Verification")

    st.title("💊 AI Medical Prescription Verification")
    
    # Custom CSS for a better UI experience
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #0056b3;
            transform: translateY(-2px);
        }
        .stMarkdown h3 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 5px;
        }
        .alert-box {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 5px;
            border-left: 5px solid;
        }
        .alert-success {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
        .alert-warning {
            background-color: #fff3cd;
            border-color: #ffeeba;
            color: #856404;
        }
        .alert-danger {
            background-color: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.header("Navigation")
    app_mode = st.sidebar.radio("Choose a feature", ["Drug Interaction Checker", "Dosage & Alternatives"])

    # Define the base URL for the FastAPI backend.
    BASE_URL = "http://127.0.0.1:8000"

    # Common input section for both features
    st.markdown("### Prescription Input")
    input_method = st.radio("How would you like to input the prescription?", ("Text", "Image"))

    prescription_text = ""
    if input_method == "Text":
        prescription_text = st.text_area("Enter Prescription Text", "e.g., Take Paracetamol 500mg and Warfarin 10mg daily.")
    elif input_method == "Image":
        uploaded_file = st.file_uploader("Upload an image of the prescription", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Prescription", use_column_width=True)
            # Read the image and encode it to base64
            image_data = uploaded_file.getvalue()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            # Send the base64 encoded image to the backend for OCR
            with st.spinner("Analyzing image..."):
                try:
                    ocr_response = requests.post(f"{BASE_URL}/ocr_image", json={"image_data": encoded_image})
                    ocr_response.raise_for_status()
                    prescription_text = ocr_response.json().get("text", "")
                    st.success("Image successfully processed into text.")
                    st.text_area("Extracted Text", prescription_text, height=200)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error processing image with backend: {e}. Please ensure the FastAPI backend is running.")
                    prescription_text = ""
        else:
            st.info("Please upload an image of the prescription.")

    # Feature-specific logic
    if app_mode == "Drug Interaction Checker":
        st.header("Drug Interaction Checker")
        if st.button("Check Interactions"):
            if not prescription_text:
                st.warning("Please enter a prescription or upload a valid image.")
            else:
                try:
                    response = requests.post(f"{BASE_URL}/check_interactions",
                                             json={"text": prescription_text})
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data['interactions']:
                        st.success("No significant drug interactions detected.")
                    else:
                        st.markdown("### Potential Drug Interactions Found:")
                        for interaction in data['interactions']:
                            st.markdown(f"""
                                <div class="alert-box alert-danger">
                                    **Interaction between {interaction['drug1']} and {interaction['drug2']}**
                                    <br>
                                    Description: {interaction['description']}
                                    <br>
                                    **Alert:** {interaction['alert']}
                                </div>
                            """, unsafe_allow_html=True)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error communicating with the backend: {e}. Please ensure the FastAPI backend is running.")

    elif app_mode == "Dosage & Alternatives":
        st.header("Dosage & Alternatives")
        age = st.number_input("Enter Patient's Age", min_value=1, max_value=120, value=30)
        
        if st.button("Check Dosage and Alternatives"):
            if not prescription_text:
                st.warning("Please enter a prescription or upload a valid image.")
            else:
                try:
                    response = requests.post(f"{BASE_URL}/dosage_alternatives",
                                             json={"text": prescription_text, "age": age})
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data['results']:
                        st.warning("No drug information could be retrieved.")
                    else:
                        st.markdown("### Dosage and Alternative Recommendations:")
                        for result in data['results']:
                            st.subheader(f"Drug: {result['drug']} (RxCUI: {result['rxcui']})")
                            st.write(f"**Dosage Status:** {result['dosage_status']}")
                            st.write(f"**Valid Dosage Forms:** {', '.join(result['dosage_forms'])}")
                            if result['alternatives']:
                                st.write(f"**Safe Alternatives:** {', '.join(result['alternatives'])}")
                            else:
                                st.write("**Safe Alternatives:** None found.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error communicating with the backend: {e}. Please ensure the FastAPI backend is running.")

if __name__ == '__main__':
    main()
