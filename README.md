# CognitiveX Project - Medical Prescription Verification

🏥 **AI-Powered Medical Prescription Analysis using IBM Models from Hugging Face**

## Overview

This project provides an intelligent medical prescription verification system that leverages IBM's powerful models hosted on Hugging Face, eliminating the need for IBM Watson API keys while maintaining enterprise-grade AI capabilities.

## Key Features

- **IBM Granite Models**: Utilizes IBM's latest Granite models for medical text analysis
- **Medical Entity Recognition**: Advanced NER using specialized biomedical models
- **No API Keys Required**: Many IBM models on Hugging Face work without authentication
- **Modern Web Interface**: Streamlit-based frontend for easy interaction
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **File Upload Support**: Handles text files and images
- **Real-time Analysis**: Fast prescription processing and verification

## Available IBM Models

- **IBM Granite 3.0 2B Instruct**: `ibm-granite/granite-3.0-2b-instruct`
- **IBM Granite 3.0 8B Instruct**: `ibm-granite/granite-3.0-8b-instruct` (Medical-focused)
- **BioBERT Chemical NER**: `alvaroalon2/biobert_chemical_ner`
- **Biomedical NER**: `d4data/biomedical-ner-all`

## Technology Stack

- **Backend**: FastAPI, Python 3.12
- **Frontend**: Streamlit
- **AI Models**: IBM Granite, BioBERT, Hugging Face Transformers
- **Dependencies**: PyTorch, Transformers, Tokenizers

## Quick Start

### Prerequisites

- Python 3.12+
- Pip package manager

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd /workspaces/CognitiveX-Project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install streamlit
   ```

3. **Configure environment (optional):**
   ```bash
   # Edit .env file - HuggingFace API key is optional for many models
   # Many IBM models work without authentication
   ```

### Running the Application

#### Option 1: Full Stack (Recommended)
```bash
# Terminal 1: Start FastAPI Backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Streamlit Frontend
python -m streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

#### Option 2: Using the run script
```bash
python run.py
```

### Access the Application

- **Streamlit Web Interface**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Core Endpoints

- `GET /` - System status and available models
- `GET /models` - List all available IBM models
- `GET /health` - Health check

### Analysis Endpoints

- `POST /analyze-prescription` - Complete prescription analysis
- `POST /extract-drug-info` - Extract drug names and information
- `POST /analyze-text` - Direct text analysis
- `POST /granite-chat` - Chat with IBM Granite model

### Example Usage

```bash
# Test system status
curl -X GET "http://localhost:8000/"

# Analyze text with IBM models
curl -X POST "http://localhost:8000/analyze-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Take aspirin 325mg twice daily for pain relief"

# Chat with IBM Granite
curl -X POST "http://localhost:8000/granite-chat" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=What are the side effects of aspirin?"
```

## Advantages of Using IBM Models via Hugging Face

1. **No IBM Cloud Account Required**: Direct access to IBM models
2. **Free Tier Available**: Many models work without API keys
3. **Enterprise Quality**: IBM's production-grade models
4. **Easy Integration**: Standard Hugging Face API
5. **Scalable**: Upgrade to Hugging Face Pro for faster inference
6. **Open Source Friendly**: Transparent model access
- **User-friendly Interface**: Streamlit-based web application

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the application:
```bash
python run.py
```

## API Endpoints

- `GET /`: Health check
- `POST /analyze-prescription`: Analyze uploaded prescription
- `POST /extract-drug-info`: Extract drug information from text

## Configuration

Set the following environment variables in `.env`:

- `IBM_WATSON_API_KEY`: Your IBM Watson API key
- `IBM_WATSON_URL`: Your IBM Watson service URL
- `HUGGING_FACE_API_KEY`: Your Hugging Face API token

## Usage

1. Start the application with `python run.py`
2. Open http://localhost:8501 in your browser
3. Upload a prescription or enter text
4. View analysis results from both IBM Watson and Hugging Face models

## Architecture

- **Backend**: FastAPI for REST API endpoints
- **Frontend**: Streamlit for user interface
- **AI Services**: IBM Watson NLU + Hugging Face Transformers
- **Integration**: RESTful API communication between components