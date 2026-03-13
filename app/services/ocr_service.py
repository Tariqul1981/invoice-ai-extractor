import pytesseract
from pdf2image import convert_from_path


def extract_text_with_ocr(file_path: str) -> str:
    text = ""
    try:
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image)
    except Exception as e:
        print("OCR extraction error:", e)
    return text