from transformers import pipeline

generator = None

def load_model():
    global generator

    if generator is None:

        generator = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad"
        )


def generate_answer(context, query):

    load_model()

    result = generator(
        question=query,
        context=context if context else "No context found"
    )

    return result["answer"]