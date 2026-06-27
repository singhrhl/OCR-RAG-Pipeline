# 📄 OCR-to-RAG Document Intelligence System

An end-to-end **OCR → Retrieval Augmented Generation (RAG)** pipeline that converts scanned PDFs/images into **searchable documents** and enables **natural language question answering**.

The system extracts structured text using OCR, generates **searchable PDFs with invisible text layers**, builds semantic embeddings, and answers questions using an LLM.

---

# 🎯 Objective

Build a system that:

* Accepts scanned **PDF/Image documents**
* Extracts text using OCR
* Generates **searchable PDFs**
* Stores document embeddings
* Enables semantic search
* Answers user questions using LLM

---

# 🧠 System Architecture

```
                User Interface (Streamlit)
                         │
                         ▼
                FastAPI Backend Server
                         │
     ┌───────────────────┼───────────────────┐
     ▼                   ▼                   ▼
Preprocessing        OCR Engine        PDF Generator
(OpenCV)           (Tesseract)         (ReportLab)
     │                   │                   │
     ▼                   ▼                   ▼
 Image Cleanup     Text + Bounding     Searchable PDF
                   Boxes Extraction     Generation
                         │
                         ▼
                  Embedding Engine
            (Sentence Transformers)
                         │
                         ▼
                    FAISS Index
                         │
                         ▼
                    Query Engine
                         │
                         ▼
                     LLM Model
                 (DistilBERT QA)
                         │
                         ▼
                       Answer
```

---

# ✨ Features

## 📂 Document Processing

* Upload **PDF or Images**
* Automatic preprocessing
* Noise removal
* Grayscale normalization
* OCR text extraction
* Bounding box detection

---

## 📄 Searchable PDF Generation

Generated PDFs include:

✔ Original image background
✔ Invisible text layer
✔ Selectable text
✔ Ctrl+F Search
✔ OCR bounding box alignment

Meets assignment requirement:

> Compose output PDFs with original image as background and invisible selectable text aligned to OCR bounding boxes.

---

## 🔎 Retrieval Augmented Generation

Pipeline:

```
User Query
   ↓
Vector Search (FAISS)
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

---

## 🤖 LLM Question Answering

Model used:

```
distilbert-base-cased-distilled-squad
```

Advantages:

* Fast
* Lightweight
* CPU compatible
* Accurate QA

File:

```
app/llm.py
```

---

# 🖥 User Interface

Interactive UI built using **Streamlit**.

<img width="1919" height="1003" alt="image" src="https://github.com/user-attachments/assets/33c2df09-a584-423b-a131-9519c9b16985" />
<img width="1916" height="1000" alt="image" src="https://github.com/user-attachments/assets/9718fedd-dc9c-4b7c-8c3d-27cd76f728e3" />

Users can:

✔ Upload documents
✔ Process OCR
✔ Ask questions
✔ View answers
✔ Download searchable PDF

Run UI:

```
streamlit run frontend.py
```

Access:

```
http://localhost:8501
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```
git clone <repo-url>
cd OCR-RAG-Pipeline
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

Linux/Mac:

```
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

# ⚠️ Install Poppler (Required for PDF)

Download:

```
https://github.com/oschwartz10612/poppler-windows/releases
```

Extract:

```
C:\poppler
```

Update in:

```
app/main.py
```

```
poppler_path=r"C:\poppler\Library\bin"
```

Required for:

```
PDF → Image conversion
```

---

# ▶️ Running Backend

Start FastAPI server:

```
uvicorn app.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger API:

```
http://127.0.0.1:8000/docs
```

---

# 📤 API Endpoints
<img width="1903" height="959" alt="image" src="https://github.com/user-attachments/assets/9db102e1-3790-4d35-bcad-ad4dc032d663" />

## Upload Document

```
POST /upload
```

Returns:

```
{
 "status":"processed",
 "pdf":"path"
}
```

---

## Query Document

```
GET /query?q=your_question
```

Returns:

```
{
 "answer":"..."
}
```

---

## Download PDF

```
GET /download?filename=file.pdf
```

---

# 📁 Project Structure

```
OCR-RAG-Pipeline
│
├── app
│   ├── main.py
│   ├── preprocess.py
│   ├── ocr_engine.py
│   ├── pdf_generator.py
│   ├── rag.py
│   ├── llm.py
│
├── data
│   ├── uploads
│   ├── processed
│
├── frontend.py
├── requirements.txt
└── README.md
```

---

# 🔬 OCR Pipeline

### Preprocessing

* Grayscale conversion
* Noise reduction
* Thresholding
* Contrast enhancement

File:

```
preprocess.py
```

---

### OCR Extraction

Uses:

```
Tesseract OCR
```

Extracts:

* Text
* Bounding boxes

File:

```
ocr_engine.py
```

---

# 📄 Searchable PDF Pipeline

Steps:

```
Image
  ↓
OCR Text + Boxes
  ↓
Invisible Text Overlay
  ↓
Searchable PDF
```

File:

```
pdf_generator.py
```

Supports:

✔ Text selection
✔ Ctrl+F search
✔ Invisible text layer

---

# 🔎 RAG Pipeline

Steps:

### 1️⃣ Text Chunking

Document text split into chunks.

### 2️⃣ Embeddings

Model:

```
sentence-transformers
```

### 3️⃣ Vector Store

Library:

```
FAISS
```

### 4️⃣ Retrieval

Top-k similar chunks returned.

File:

```
rag.py
```

---

# 🧠 LLM Pipeline

Steps:

```
User Query
  ↓
Retrieved Context
  ↓
DistilBERT QA Model
  ↓
Answer
```

Model:

```
distilbert-base-cased-distilled-squad
```

Advantages:

✔ CPU compatible
✔ Fast inference
✔ Low memory

---

# 📊 Example Queries

```
What is the course name?

Who is the supervisor?

What is the date?

What is the topic of quiz?
```

---

# ✅ Project Requirements Coverage

| Requirement                | Status |
| -------------------------- | ------ |
| OCR extraction             | ✅      |
| Bounding boxes             | ✅      |
| Searchable PDF             | ✅      |
| Invisible text             | ✅      |
| Image background preserved | ✅      |
| RAG pipeline               | ✅      |
| LLM QA                     | ✅      |
| API endpoints              | ✅      |
| UI interface               | ✅      |

---

# ⚡ Performance

| Step       | Time    |
| ---------- | ------- |
| OCR        | 2–5 sec |
| Embeddings | 1 sec   |
| Query      | <1 sec  |

CPU-only compatible.

---

# 🧰 Technologies Used

### Backend

* FastAPI
* Python

### AI

* Transformers
* SentenceTransformers
* FAISS

### OCR

* Tesseract
* OpenCV

### PDF

* ReportLab

### Frontend

* Streamlit

---

# 📸 Example Output

### Input Document

Scanned exam paper or letter.

### Output

✔ Searchable PDF
✔ Invisible text
✔ QA enabled

---

# 👨‍💻 Author

Deepesh Lodhi
IIT Delhi
