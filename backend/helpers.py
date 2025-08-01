# ai_medical_checker/backend/helpers.py

import os
import requests
import pandas as pd
import base64
from typing import List, Dict, Optional
import streamlit as st
import io
from PIL import Image

# This file contains all the helper functions for the backend.
# It is responsible for interacting with external APIs and loading the dataset.

# --- Data Loading ---
def load_ddi_dataset(file_path: str) -> pd.DataFrame:
    """
    Loads the pre-processed drug-drug interaction dataset.
    This file should be generated as per the project documentation.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Please ensure "
              "you have generated it as per Milestone 1.")
        return pd.DataFrame()

ddi_df = load_ddi_dataset(os.path.join(os.path.dirname(__file__), "..", "data", "ddi_mapped_with_rxcui.csv"))
if ddi_df.empty:
    print("Warning: DDI dataset is empty. Interaction checking will not work.")

# --- OCR Integration (Image to Text) ---
def ocr_image_to_text(base64_image: str) -> str:
    """
    A placeholder function for an OCR service.
    """
    # Placeholder for a real API call.
    print("Simulating OCR to text conversion...")
    
    # In a real scenario, you would make an API call here.
    # For now, let's just return some mock text.
    return "Paracetamol 500mg daily. Warfarin 10mg. Prescription for a patient over 60."

# --- Hugging Face Integration (Drug Extraction) ---
def query_hugging_face_ner(text: str) -> List[str]:
    """
    TEMPORARY FIX: A placeholder that returns hardcoded drugs.
    The original API call is commented out below.
    This allows the application to run even without a valid API key.
    """
    print("Simulating Hugging Face NER model call...")
    # This will return a hardcoded list of drugs for demonstration purposes.
    return ["Paracetamol", "Warfarin"]
    
    # ORIGINAL API CALL (commented out)
    # HUGGING_FACE_API_KEY = st.secrets["HUGGING_FACE_API_KEY"]
    # HUGGING_FACE_NER_URL = st.secrets["HUGGING_FACE_NER_URL"]

    # headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    # payload = {"inputs": text}
    # try:
    #     response = requests.post(HUGGING_FACE_NER_URL, headers=headers, json=payload)
    #     response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     print(f"Hugging Face API Error: {e}")
    #     return []

    # result = response.json()
    # extracted_drugs = set()
    # for entity in result:
    #     if entity['entity_group'] == 'MEDICINE':
    #         extracted_drugs.add(entity['word'].replace(' ', ''))
    
    # return list(extracted_drugs)


# --- IBM Granite NLP for Alerts ---
def get_ibm_granite_alerts(text: str) -> str:
    """
    Analyzes interaction text using a placeholder for the ibm-granite model.
    This demonstrates the functionality without requiring a paid API key.
    A real implementation would involve an API call to the model.
    """
    print(f"Simulating ibm-granite model call for text: {text}")
    
    # Placeholder logic based on keywords
    text_lower = text.lower()
    if 'increase' in text_lower or 'risk' in text_lower or 'harmful' in text_lower or 'severe' in text_lower:
        return "❗️ Severe interaction detected. Immediate consultation advised."
    elif 'decrease' in text_lower or 'monitor' in text_lower or 'caution' in text_lower:
        return "⚠️ High-risk interaction detected. Use with caution."
    else:
        return "✅ No severe interaction risk detected. Monitor patient as usual."

# --- RxNorm Integration ---
def get_rxcui(drug_name: str) -> Optional[str]:
    """
    Fetches the RxCUI for a given drug name from the RxNorm API.
    """
    RXNORM_API_BASE_URL = "https://rxnav.nlm.nih.gov/REST"
    url = f"{RXNORM_API_BASE_URL}/rxcui.json"
    params = {"name": drug_name}
    print(f"Attempting to get RxCUI for '{drug_name}'...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'idGroup' in data and 'rxnormId' in data['idGroup']:
            rxcui = data['idGroup']['rxnormId'][0]
            print(f"Successfully found RxCUI: {rxcui}")
            return rxcui
        else:
            print(f"No RxCUI found for '{drug_name}'. Response: {data}")
            return None
    except requests.RequestException as e:
        print(f"RxNorm API error for {drug_name}: {e}")
    return None

def get_dosage_forms(rxcui: str) -> List[str]:
    """
    Fetches dosage forms for a given RxCUI.
    """
    RXNORM_API_BASE_URL = "https://rxnav.nlm.nih.gov/REST"
    url = f"{RXNORM_API_BASE_URL}/rxcui/{rxcui}/related.json"
    params = {"tty": "SCD"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'relatedGroup' in data and 'conceptGroup' in data['relatedGroup']:
            forms = [concept['name'] for concept in data['relatedGroup']['conceptGroup'][0]['conceptProperties']]
            return forms
    except requests.RequestException as e:
        print(f"RxNorm API error for dosage forms: {e}")
    return []

def get_alternatives(rxcui: str) -> List[str]:
    """
    Finds alternative drugs with the same active ingredient.
    """
    RXNORM_API_BASE_URL = "https://rxnav.nlm.nih.gov/REST"
    ingredient_rxcui = None
    url = f"{RXNORM_API_BASE_URL}/rxcui/{rxcui}/related.json"
    params = {"tty": "IN"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'relatedGroup' in data and 'conceptGroup' in data['relatedGroup']:
            ingredient_rxcui = data['relatedGroup']['conceptGroup'][0]['conceptProperties'][0]['rxcui']
    except requests.RequestException as e:
        print(f"RxNorm API error for alternatives: {e}")
        return []

    if not ingredient_rxcui:
        return []

    url = f"{RXNORM_API_BASE_URL}/rxcui/{ingredient_rxcui}/related.json"
    params = {"tty": "SBD"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'relatedGroup' in data and 'conceptGroup' in data['relatedGroup']:
            alternatives = [concept['name'] for concept in data['relatedGroup']['conceptGroup'][0]['conceptProperties']]
            return alternatives
    except requests.RequestException as e:
        print(f"RxNorm API error for alternatives: {e}")
    return []
