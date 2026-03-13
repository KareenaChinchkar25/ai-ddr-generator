import fitz
import os


def extract_text_and_images(pdf_path, image_dir):
    doc = fitz.open(pdf_path)
    text = ""

    os.makedirs(image_dir, exist_ok=True)

    for page_index in range(len(doc)):
        page = doc[page_index]

        text += page.get_text()

        images = page.get_images()

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_path = f"{image_dir}/page{page_index}_img{img_index}.png"

            with open(image_path, "wb") as f:
                f.write(image_bytes)

    return text
