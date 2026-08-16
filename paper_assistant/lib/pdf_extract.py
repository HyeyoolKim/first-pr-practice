from pypdf import PdfReader


def extract_text(file) -> str:
    reader = PdfReader(file)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages).strip()
