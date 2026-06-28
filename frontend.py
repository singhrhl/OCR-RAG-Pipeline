import streamlit as st
import requests
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

st.title("📄 OCR → RAG Document Assistant")

st.write("Upload Image/PDF → Ask Questions → Get Answers")

# -------------------
# Upload Section
# -------------------

st.header("Upload Document")

uploaded_file = st.file_uploader(
    "Upload JPG, PNG or PDF",
    type=["jpg","jpeg","png","pdf"]
)

if uploaded_file is not None:

    st.success("File selected")

    if st.button("Process Document"):

        files = {"file": uploaded_file.getvalue()}

        response = requests.post(
            f"{BACKEND_URL}/upload",
            files={"file":uploaded_file}
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Processing Completed")

            st.write("Generated PDF:")

            st.write(result["pdf"])

            st.session_state["pdf"] = result["pdf"]

        else:

            st.error("Upload failed")


# -------------------
# Query Section
# -------------------

st.header("Ask Questions")

query = st.text_input("Enter Question")

if st.button("Ask"):

    response = requests.get(
        f"{BACKEND_URL}/query",
        params={"q":query}
    )

    if response.status_code == 200:

        answer = response.json()["answer"]

        st.success("Answer:")

        st.write(answer)

    else:

        st.error("Query failed")


# -------------------
# Download PDF
# -------------------

st.header("Download Processed PDF")

if "pdf" in st.session_state:

    pdf_path = st.session_state["pdf"]

    filename = pdf_path.split("/")[-1]

    download_url = f"{BACKEND_URL}/download?filename={filename}"

    if st.button("Download PDF"):

        pdf = requests.get(download_url)

        st.download_button(
            "Click to Save",
            pdf.content,
            file_name=filename
        )