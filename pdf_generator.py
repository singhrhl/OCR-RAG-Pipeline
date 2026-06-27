from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image


def create_pdf(image_path, text, boxes, output_pdf):

    c = canvas.Canvas(output_pdf, pagesize=letter)

    width, height = letter

    # Draw background image
    c.drawImage(image_path, 0, 0, width=width, height=height)

    # Invisible text layer
    c.setFont("Helvetica", 8)
    c._code.append("3 Tr")

    img = Image.open(image_path)
    img_w, img_h = img.size

    scale_x = width / img_w
    scale_y = height / img_h

    for box in boxes:

        try:
            # Format 1 → dict with bbox
            if isinstance(box, dict):

                word = box.get("text","")

                bbox = box.get("bbox",[0,0,0,0])

                x = bbox[0]
                y = bbox[1]

            # Format 2 → tuple
            else:

                word = box[0]
                x = box[1]
                y = box[2]

            pdf_x = x * scale_x
            pdf_y = height - (y * scale_y)

            c.drawString(pdf_x, pdf_y, word)

        except:
            continue

    c._code.append("0 Tr")

    c.save()

    return output_pdf