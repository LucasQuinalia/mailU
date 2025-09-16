import pdfplumber
import io

def read_file_content(filename: str, content: bytes) -> str:
    if filename.endswith(".txt"):
        return content.decode("utf-8")

    elif filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    return ""
