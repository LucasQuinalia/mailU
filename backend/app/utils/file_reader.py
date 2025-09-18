import pdfplumber
import io

def read_file_content(filename: str, content: bytes) -> str:
    try:
        if filename.endswith(".txt"):
            return content.decode("utf-8")

        elif filename.endswith(".pdf"):
            text = ""
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()

        return ""
    except Exception as e:
        print(f"Erro ao ler arquivo {filename}: {str(e)}")
        return ""
