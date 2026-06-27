import os
import shutil

from dotenv import load_dotenv
load_dotenv()  # reads .env in the project root, if present; no-op if missing

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.preprocess import preprocess_image
from app.ocr_engine import extract_text
from app.pdf_generator import create_pdf
from app.rag import store_embeddings, search
from app.llm import generate_answer

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "data/uploads/"
PROC_DIR = "data/processed/"

# On Linux/Docker, poppler-utils installs to a location already on PATH,
# so pdf2image finds it automatically when poppler_path=None.
# On Windows, set POPPLER_PATH in your environment (or a .env file) to
# the `bin` folder of your local poppler install, e.g.:
#   POPPLER_PATH=C:\poppler\Library\bin
POPPLER_PATH = os.environ.get("POPPLER_PATH") or None


@app.get("/")
def home():
    return {"message": "OCR RAG Pipeline Running"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    path = str(UPLOAD_DIR) + file.filename

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # If PDF convert to image
    if file.filename.endswith(".pdf"):

        from pdf2image import convert_from_path

        pages = convert_from_path(
            path,
            poppler_path=POPPLER_PATH
        )

        text = ""

        for i, page in enumerate(pages):

            image_path = PROC_DIR + f"page{i+1}.jpg"

            page.save(image_path, "JPEG")

            proc = preprocess_image(image_path)

            page_text, boxes = extract_text(proc)

            text += page_text + "\n"

        image_path = PROC_DIR + "page1.jpg"

    else:

        image_path = path

        proc = preprocess_image(image_path)

        text, boxes = extract_text(proc)

    pdf_path = str(PROC_DIR) + file.filename + ".pdf"

    create_pdf(image_path, text, boxes, pdf_path)

    store_embeddings(text)

    return {
        "status": "processed",
        "pdf": pdf_path
    }


@app.get("/query")
def query(q: str):

    contexts = search(q)

    context = " ".join(contexts)

    answer = generate_answer(context, q)

    return {
        "answer": answer
    }

@app.get("/download")
def download(filename: str):
    pdf_path = PROC_DIR + filename
    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)

@app.get("/preview/{filename}")
def preview(filename: str):
    img_path = PROC_DIR + filename
    return FileResponse(img_path, media_type="image/jpeg")