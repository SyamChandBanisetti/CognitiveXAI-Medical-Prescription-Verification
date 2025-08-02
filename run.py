import subprocess
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

def run_fastapi():
    """Run FastAPI backend"""
    host = os.getenv('FASTAPI_HOST', '0.0.0.0')
    port = os.getenv('FASTAPI_PORT', '8000')
    subprocess.run([
        'uvicorn', 
        'app.main:app', 
        '--host', host, 
        '--port', port, 
        '--reload'
    ])

def run_streamlit():
    """Run Streamlit frontend"""
    time.sleep(3)  # Wait for FastAPI to start
    subprocess.run([
        'streamlit', 
        'run', 
        'streamlit_app.py', 
        '--server.port', '8501',
        '--server.address', '0.0.0.0'
    ])

if __name__ == "__main__":
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    print("Starting FastAPI backend...")
    print("FastAPI will be available at: http://localhost:8000")
    
    # Start Streamlit in main thread
    print("Starting Streamlit frontend...")
    print("Streamlit will be available at: http://localhost:8501")
    
    run_streamlit()
