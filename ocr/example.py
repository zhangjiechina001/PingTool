import pytesseract
from PIL import Image

# Open an image using the Python Imaging Library (PIL)
image = Image.open('img1.png')
pytesseract.pytesseract.tesseract_cmd='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)