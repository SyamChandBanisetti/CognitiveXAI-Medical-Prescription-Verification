#!/bin/bash

echo "🚀 Starting Medical Prescription Verification API..."

# Navigate to project directory
cd /workspaces/CognitiveX-Project

# Install dependencies if not already installed
echo "📦 Installing dependencies..."
pip install fastapi uvicorn python-dotenv requests ibm-watson python-multipart

# Start the server
echo "🔥 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
