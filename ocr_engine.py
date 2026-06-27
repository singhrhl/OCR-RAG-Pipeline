import easyocr

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):

    results = reader.readtext(image_path)

    text = ""

    boxes = []

    for result in results:

        bbox = result[0]
        detected_text = result[1]
        confidence = result[2]

        text += detected_text + " "

        boxes.append({
            "text": detected_text,
            "bbox": bbox,
            "confidence": confidence
        })

    return text, boxes