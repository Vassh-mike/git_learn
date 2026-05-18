import fitz
import pandas as pd
from docx import Document
from PIL import Image
import pytesseract


def extract_text(uploaded_file):

    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return parse_pdf(uploaded_file)

    elif name.endswith(".docx"):
        return parse_docx(uploaded_file)

    elif name.endswith(".xlsx"):
        return parse_excel(uploaded_file)

    elif name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif name.endswith((".png", ".jpg", ".jpeg")):
        return parse_image(uploaded_file)

    else:
        return "Unsupported format"


def parse_pdf(file):

    text = ""

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    return text


def parse_docx(file):

    doc = Document(file)

    return "\n".join(
        [p.text for p in doc.paragraphs]
    )


def parse_excel(file):

    df = pd.read_excel(file)

    return df.to_string()


def parse_image(file):

    image = Image.open(file)

    return pytesseract.image_to_string(image)