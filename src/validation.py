from datetime import datetime


def validate_document(document):
    errors = []

    # Check required fields
    if not document["name"]:
        errors.append("Name is missing")

    if not document["document_id"]:
        errors.append("Document ID is missing")

    if not document["dob"]:
        errors.append("Date of birth is missing")

    if not document["expiry_date"]:
        errors.append("Expiry date is missing")

    # Check expiry date
    try:
        expiry = datetime.strptime(
            document["expiry_date"],
            "%d-%m-%Y"
        )

        today = datetime.today()

        if expiry < today:
            errors.append("Document has expired")

    except ValueError:
        errors.append("Invalid expiry date format")

    return errors