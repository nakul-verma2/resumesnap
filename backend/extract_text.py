import os
import pymupdf as fitz
import re
from dataclasses import dataclass
from typing import List, Union
from backend import ocr as o


@dataclass
class ExtractedData:
    file_path: str
    file_type: str
    cleaned_text: str

def extract_pdf_text(pdf_path: str) -> str:
    try:
        with fitz.open(pdf_path) as doc:
            return "\n".join(page.get_text("text").strip() for page in doc)
    except Exception as e:
        return f"Error extracting text: {e}"

def clean_text(text: str) -> str:
    text = re.sub(r'\b\w\b', '', text)  
    text = re.sub(r'[^\x20-\x7E\n]', '', text)  
    return text.strip()

def check_file_type_and_extract(filepath: str) -> ExtractedData:
    file_extension = os.path.splitext(filepath.lower())[1]

    if file_extension in {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}:
        file_type, extracted_text = "image", o.perform_ocr(filepath)
        print("Extracted text from PDF suing ocr")

    elif file_extension == '.pdf':
        with fitz.open(filepath) as doc:
            text = doc[0].get_text("text").strip()
            file_type = "pdf_text" if text else "pdf_image"
            if text:
                extracted_text = extract_pdf_text(filepath)
                print("Extracted text from PDF suing fitz")
            else:
                extracted_text = o.perform_ocr_pdf(filepath)
                print("Extracted text from PDF suing ocr")
    else:
        return ExtractedData(filepath, "unsupported", "Unsupported file type. Please upload a PDF or image file.")

    return ExtractedData(filepath, file_type, clean_text(extracted_text))

def process_files(file_paths: Union[str, List[str]]) -> List[ExtractedData]:
    if not file_paths:
        return []

    files = [file_paths] if isinstance(file_paths, str) else file_paths
    return [check_file_type_and_extract(file) for file in files]

