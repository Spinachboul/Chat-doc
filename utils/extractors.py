import pytesseract
from PIL import Image
import fitz
import io

async def extract_content(file):
    filename = file.filename.lower()
    data = await file.read()

    if filename.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")
    
    elif filename.endswith(".jpg", "jpeg" , "png"):
        image = Image.open(io.BytesIO(data))
        text = pytesseract.image_to_string(image)
        return text.strip()

    elif filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(data)
        
        text = ""
        doc = fitz.open("temp.pdf")
        for page in doc:
            text += page.get_text()
        
        return text.strip()

    else:
        return
