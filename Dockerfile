FROM python:3.11-slim

# System dependencies:
# - poppler-utils: required by pdf2image for PDF -> image conversion
# - libgl1, libglib2.0-0: required by opencv-python (cv2) at runtime
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /code

# Install Python dependencies first (separate layer so Docker caches this
# step and doesn't reinstall ~2GB of torch/transformers on every code change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project
COPY . .

# Make sure data dirs exist even if .gitkeep files weren't copied for some reason
RUN mkdir -p data/uploads data/processed

# HF Spaces (Docker SDK) expects the app to listen on 7860
EXPOSE 7860

# Run both processes via a startup script
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]