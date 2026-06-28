#!/bin/bash
set -e

# Start FastAPI backend in the background, on an internal-only port
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend in the foreground, on the port HF Spaces exposes
streamlit run frontend.py \
  --server.port 7860 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false