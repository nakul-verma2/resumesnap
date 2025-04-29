import os
import pymupdf as fitz
import easyocr

reader = easyocr.Reader(['en'])

def perform_ocr(image_path):
    if not os.path.exists(image_path):
        return f"Error: The file '{image_path}' does not exist."
    
    result = reader.readtext(image_path, detail=0)
    return "\n".join([line.strip() for line in result if len(line) > 1])

def perform_ocr_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        result = []
        
        for i, page in enumerate(doc):
            image_path = f"temp_page_{i}.jpg"
            page.get_pixmap().save(image_path)
            result.append(perform_ocr(image_path))
            os.remove(image_path)
        
        doc.close()
        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"

        