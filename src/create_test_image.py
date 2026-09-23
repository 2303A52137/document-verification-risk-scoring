from PIL import Image, ImageDraw, ImageFont


# Create a white image
image = Image.new("RGB", (1000, 600), "white")

# Create drawing object
draw = ImageDraw.Draw(image)


# Load font
font = ImageFont.truetype("arial.ttf", 32)


# Test document with intentional problems
text = """DOCUMENT VERIFICATION TEST

Name: Rahul Kumar
Document ID:
Date of Birth: 15-08-2003
Expiry Date: 15-08-2023
Country: India
"""


# Draw text on image
draw.multiline_text(
    (50, 50),
    text,
    fill="black",
    font=font,
    spacing=20
)


# Save the test document
image.save("input_documents/test_document.png")

print("Invalid test document created successfully!")