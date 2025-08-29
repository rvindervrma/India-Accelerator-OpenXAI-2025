import pdfplumber


def extract_text_from_pdf(pdf_path: str):
    text_chunks = []
    pages = 0
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages += 1
            txt = page.extract_text() or ""
            text_chunks.append(txt)
    full_text = "\n\n".join(text_chunks)
    return full_text, {"pages": pages, "chars": len(full_text)}