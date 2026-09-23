import pytesseract
from PIL import Image

# Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Open our test document
image = Image.open("input_documents/test_document.png")

# Extract text from the image
text = pytesseract.image_to_string(image)

# Display the extracted text
print("----- EXTRACTED TEXT -----")
print(text)
print("--------------------------")