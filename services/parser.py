from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file_path):
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text(file_path, extension):

    if extension == "pdf":
        return extract_pdf_text(file_path)

    elif extension == "docx":
        return extract_docx_text(file_path)

    else:
        raise ValueError("Unsupported file type.")