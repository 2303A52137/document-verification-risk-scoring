# Document Verification & Risk Scoring

A simple document verification system that uses OCR to extract information from uploaded documents, validates the extracted data, and assigns a risk score.

## How it works

Document → OCR → Field Extraction → Validation → Risk Score → Result

The system can classify documents as:

- ✅ VERIFIED
- ⚠️ FLAGGED
- ❌ REJECTED

## Tech Stack

- Python
- FastAPI
- Tesseract OCR
- PyMuPDF
- SQLite
- Regular Expressions

## Features

- Upload PDF or image documents
- Extract text using OCR
- Extract important fields
- Validate missing and expired information
- Calculate a rule-based risk score
- Store verification history in SQLite
- REST API with Swagger documentation

## Run the Project

```bash
pip install -r requirements.txt
uvicorn src.api:app --reload
