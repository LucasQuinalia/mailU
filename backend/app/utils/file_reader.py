import pdfplumber
import io

def read_file_content(filename: str, content: bytes) -> str:
    try:
        if filename.lower().endswith(".txt"):
            return content.decode("utf-8")

        elif filename.lower().endswith(".pdf"):
            text = ""
            try:
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        try:
                            page_text = page.extract_text()
                            if page_text and page_text.strip():
                                text += page_text + "\n"
                        except Exception as page_error:
                            print(f"Erro na página {page_num + 1}: {str(page_error)}")
                            continue
                
                if text.strip():
                    return text.strip()
                else:
                    print("PDF não contém texto extraível")
                    return ""
                    
            except Exception as pdf_error:
                print(f"Erro ao processar PDF: {str(pdf_error)}")
                return ""

        return ""
    except Exception as e:
        print(f"Erro ao ler arquivo {filename}: {str(e)}")
        return ""
