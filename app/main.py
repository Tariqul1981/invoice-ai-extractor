from app.services.schema import InvoiceSchema

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from app.services.pdf_service import extract_text_from_pdf
from app.services.ocr_service import extract_text_with_ocr
from app.services.ai_service import extract_invoice_data

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_model=InvoiceSchema)
async def upload_invoice(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    if len(text.strip()) < 50:
        text = extract_text_with_ocr(file_path)

    if not text.strip():
        return JSONResponse({"error": "Could not extract text from invoice."})

    result = extract_invoice_data(text)

    if "error" in result:
        return JSONResponse(result)

    try:
        validated = InvoiceSchema.model_validate(result)
        return validated.model_dump()
    except Exception as e:
        return JSONResponse({
            "error": "Schema validation failed",
            "details": str(e),
            "ai_output": result
        })

    os.remove(file_path)

    return {"extracted_data": result}