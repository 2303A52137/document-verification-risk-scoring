import pytesseract
from PIL import Image

from extract_fields import extract_fields
from validation import validate_document
from risk_scoring import calculate_risk, get_status
from database import create_database, save_result


# ============================================================
# DOCUMENT VERIFICATION SYSTEM
# ============================================================

# 1. Create the database if it does not already exist
create_database()


# 2. Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# 3. Document location
document_path = "input_documents/test_document.png"


# 4. Open the document
image = Image.open(document_path)


# 5. OCR - Convert document image into text
text = pytesseract.image_to_string(image)

print("\n===== OCR OUTPUT =====")
print(text)
print("======================")


# 6. Extract important fields from OCR text
fields = extract_fields(text)

print("\n===== EXTRACTED FIELDS =====")

for key, value in fields.items():
    print(f"{key}: {value}")

print("============================")


# 7. Validate the extracted information
errors = validate_document(fields)

print("\n===== VALIDATION RESULT =====")

if len(errors) == 0:
    print("Document passed validation")
else:
    print("Problems found:")

    for error in errors:
        print("-", error)

print("=============================")


# 8. Calculate risk score
risk_score = calculate_risk(errors)


# 9. Determine final verification status
status = get_status(risk_score)


print("\n===== RISK ASSESSMENT =====")
print("Risk Score:", risk_score, "/ 100")
print("Status:", status)
print("===========================")


# 10. Save verification result into SQLite database
save_result(
    fields,
    risk_score,
    status,
    errors
)


print("\nResult saved to database successfully!")