from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

texts = []

index = faiss.IndexFlatL2(384)


def store_embeddings(text):

    global texts

    chunks = text.split("\n")

    texts.extend(chunks)

    embeddings = model.encode(chunks)

    index.add(np.array(embeddings))


def search(query):

    if len(texts) == 0:
        return []

    query_vec = model.encode([query])

    D, I = index.search(np.array(query_vec), 3)

    results = []

    for i in I[0]:

        if i < len(texts):
            results.append(texts[i])

    return results