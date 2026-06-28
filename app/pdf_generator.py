from reportlab.pdfgen import canvas
from PIL import Image


def create_pdf(image_path, text, boxes, output_pdf):

    img = Image.open(image_path)
    img_w, img_h = img.size

    # Build the page to match the image's own aspect ratio,
    # scaled to a fixed page width.
    page_width = 612  # points, same width as Letter for consistency
    page_height = page_width * (img_h / img_w)

    c = canvas.Canvas(output_pdf, pagesize=(page_width, page_height))

    width, height = page_width, page_height

    # Draw background image (now matches canvas aspect ratio exactly)
    c.drawImage(image_path, 0, 0, width=width, height=height)

    # Invisible text layer
    c.setFont("Helvetica", 8)
    
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

            c.drawString(pdf_x, pdf_y, word, mode=3)

        except:
            continue

    c.save()

    return output_pdf