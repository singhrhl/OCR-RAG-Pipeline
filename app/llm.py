from typing import Any
from transformers import pipeline

generator: Any = None

def load_model() -> Any:
    global generator

    if generator is None:
        generator = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")  # type: ignore

    return generator


def generate_answer(context, query):

    if not context or not context.strip():
        return "No documents have been uploaded yet, or no relevant content was found for this question."

    qa_pipeline = load_model()

    result = qa_pipeline(
        question=query,
        context=context
    )

    return result["answer"]