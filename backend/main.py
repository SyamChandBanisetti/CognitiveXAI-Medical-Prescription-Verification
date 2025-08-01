# ai_medical_checker/backend/main.py

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from .helpers import (
    query_hugging_face_ner,
    get_rxcui,
    get_dosage_forms,
    get_alternatives,
    get_ibm_granite_alerts,
    ocr_image_to_text,
    ddi_df
)

# This file contains the FastAPI application instance and the API endpoints.
# It handles incoming HTTP requests from the Streamlit frontend.

api = FastAPI(title="AI Medical Prescription Verification API")

class PrescriptionText(BaseModel):
    text: str

class PrescriptionWithAge(BaseModel):
    text: str
    age: int

class ImageData(BaseModel):
    image_data: str # Base64 encoded image string

@api.post("/ocr_image")
async def ocr_image(image_data: ImageData):
    """
    Endpoint for OCR of a prescription image.
    """
    try:
        text = ocr_image_to_text(image_data.image_data)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api.post("/check_interactions")
async def check_interactions(prescription: PrescriptionText):
    """
    Endpoint for detecting drug-drug interactions.
    """
    extracted_drugs = query_hugging_face_ner(prescription.text)
    if not extracted_drugs:
        raise HTTPException(status_code=404, detail="No drugs found in the prescription.")
    
    rxcui_map = {drug: get_rxcui(drug) for drug in extracted_drugs}
    
    interactions = []
    found_rxcui = [rxcui for rxcui in rxcui_map.values() if rxcui is not None]

    if len(found_rxcui) < 2:
        return {"message": "Not enough drugs with RxCUIs found to check for interactions.",
                "interactions": []}

    for i in range(len(found_rxcui)):
        for j in range(i + 1, len(found_rxcui)):
            rxcui1 = found_rxcui[i]
            rxcui2 = found_rxcui[j]

            interaction = ddi_df[
                ((ddi_df['RxCUI_1'] == rxcui1) & (ddi_df['RxCUI_2'] == rxcui2)) |
                ((ddi_df['RxCUI_1'] == rxcui2) & (ddi_df['RxCUI_2'] == rxcui1))
            ]

            if not interaction.empty:
                for _, row in interaction.iterrows():
                    interaction_description = row['Interaction Description']
                    alert = get_ibm_granite_alerts(interaction_description)
                    interactions.append({
                        "drug1": row['Drug 1'],
                        "drug2": row['Drug 2'],
                        "rxcui1": row['RxCUI_1'],
                        "rxcui2": row['RxCUI_2'],
                        "description": interaction_description,
                        "alert": alert
                    })

    return {"message": "Interactions checked successfully.", "interactions": interactions}

@api.post("/dosage_alternatives")
async def dosage_alternatives(prescription: PrescriptionWithAge):
    """
    Endpoint for checking dosage and suggesting alternatives.
    """
    extracted_drugs = query_hugging_face_ner(prescription.text)
    if not extracted_drugs:
        raise HTTPException(status_code=404, detail="No drugs found in the prescription.")

    results = []
    for drug in extracted_drugs:
        rxcui = get_rxcui(drug)
        if rxcui:
            dosage_forms = get_dosage_forms(rxcui)
            alternatives = get_alternatives(rxcui)
            
            # Simplified dosage logic based on age (placeholder)
            dosage_status = "Appropriate"
            if prescription.age < 18 and "tablet" in prescription.text.lower():
                 dosage_status = "May need dosage adjustment for children."
            elif prescription.age > 65:
                dosage_status = "Monitor closely for elderly patients."

            results.append({
                "drug": drug,
                "rxcui": rxcui,
                "dosage_forms": dosage_forms,
                "alternatives": alternatives,
                "dosage_status": dosage_status
            })
    
    return {"message": "Dosage and alternatives checked successfully.", "results": results}
