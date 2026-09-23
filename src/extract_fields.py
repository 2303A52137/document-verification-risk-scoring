import re


def extract_fields(text):
    fields = {}

    # Name
    match = re.search(
        r"^Name:[ \t]*(.*)$",
        text,
        re.MULTILINE
    )
    fields["name"] = match.group(1).strip() if match else ""

    # Document ID
    match = re.search(
        r"^Document ID:[ \t]*(.*)$",
        text,
        re.MULTILINE
    )
    fields["document_id"] = match.group(1).strip() if match else ""

    # Date of Birth
    match = re.search(
        r"^Date of Birth:[ \t]*(.*)$",
        text,
        re.MULTILINE
    )
    fields["dob"] = match.group(1).strip() if match else ""

    # Expiry Date
    match = re.search(
        r"^Expiry Date:[ \t]*(.*)$",
        text,
        re.MULTILINE
    )
    fields["expiry_date"] = match.group(1).strip() if match else ""

    # Country
    match = re.search(
        r"^Country:[ \t]*(.*)$",
        text,
        re.MULTILINE
    )
    fields["country"] = match.group(1).strip() if match else ""

    return fields