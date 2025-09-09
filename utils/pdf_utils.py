import pdfplumber

def extract_text_from_pdf(pdf_path):
    text=""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_txt=page.extract_text()
                if page_txt:
                    text+=page_txt+'\n'
    except Exception as e:
        print(f"ERROR could not read PDF: {e}")
    
    return text.strip()    
                        