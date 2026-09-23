import os
import shutil
import sys
import io
import sqlite3

import fitz
import pytesseract

from PIL import Image

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


# --------------------------------------------------
# Allow Python to find files inside src
# --------------------------------------------------

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract_fields import extract_fields
from validation import validate_document
from risk_scoring import calculate_risk, get_status
from database import create_database, save_result


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Document Verification API",
    description="OCR-based document verification and risk scoring system",
    version="1.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# Database
# --------------------------------------------------

create_database()


# --------------------------------------------------
# Tesseract
# --------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# --------------------------------------------------
# Upload folder
# --------------------------------------------------

UPLOAD_FOLDER = "input_documents"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Document Verification API is running"
    }


# --------------------------------------------------
# PDF → Images
# --------------------------------------------------

def pdf_to_images(pdf_path):

    pdf_document = fitz.open(pdf_path)

    images = []

    for page in pdf_document:

        pixmap = page.get_pixmap()

        image_bytes = pixmap.tobytes("png")

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        images.append(image)

    pdf_document.close()

    return images


# --------------------------------------------------
# Verify Document
# --------------------------------------------------

@app.post("/verify-document")
async def verify_document(file: UploadFile = File(...)):

    if not file.filename:
        return {
            "error": "No file uploaded"
        }

    # Save uploaded document
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    extracted_text = ""


    # --------------------------------------------------
    # PDF
    # --------------------------------------------------

    if extension == ".pdf":

        images = pdf_to_images(file_path)

        for image in images:

            extracted_text += (
                pytesseract.image_to_string(image)
                + "\n"
            )


    # --------------------------------------------------
    # Image
    # --------------------------------------------------

    elif extension in [".png", ".jpg", ".jpeg"]:

        image = Image.open(file_path)

        extracted_text = (
            pytesseract.image_to_string(image)
        )


    # --------------------------------------------------
    # Unsupported file
    # --------------------------------------------------

    else:

        return {
            "error": "Unsupported file type. Use PNG, JPG, JPEG or PDF."
        }


    # --------------------------------------------------
    # Field Extraction
    # --------------------------------------------------

    fields = extract_fields(
        extracted_text
    )


    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    errors = validate_document(
        fields
    )


    # --------------------------------------------------
    # Risk Scoring
    # --------------------------------------------------

    risk_score = calculate_risk(
        errors
    )


    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    status = get_status(
        risk_score
    )


    # --------------------------------------------------
    # Save result
    # --------------------------------------------------

    save_result(
        fields,
        risk_score,
        status,
        errors
    )


    # --------------------------------------------------
    # Return result
    # --------------------------------------------------

    return {

        "filename": file.filename,

        "extracted_fields": fields,

        "validation_errors": errors,

        "risk_score": risk_score,

        "status": status
    }


# --------------------------------------------------
# Verification History
# --------------------------------------------------

@app.get("/verification-history")
def verification_history():

    connection = sqlite3.connect(
        "document_verification.db"
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            document_id,
            dob,
            expiry_date,
            country,
            risk_score,
            status,
            problems
        FROM verification_results
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return {
        "total_records": len(results),
        "records": [dict(row) for row in results]
    }