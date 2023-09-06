import qrcode
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.colors import blue
from reportlab.lib import pagesizes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def gen_certified_document(hash_text, real_doc_path, output_doc_path, file_url, default_file_path): 
    data = hash_text
    unique_id = str(uuid.uuid4())
 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True) 
    img = qr.make_image(fill_color="black", back_color="white") 
    goodPath = os.path.join(default_file_path, unique_id+"qrcode.png")
    img.save(goodPath)
 
 
    pdfmetrics.registerFont(TTFont('Helvetica', 'Helvetica.ttf')) 
    waterPath = os.path.join(default_file_path, unique_id+"watermark.pdf")
    c = canvas.Canvas(waterPath, pagesize=letter)
    img = ImageReader(goodPath)
 
    c.drawImage(img, 400, 670, width=130, height=130) 
    c.setFont('Helvetica', 11)
    c.setFillColor(blue)
 
    c.drawString(20, 10, file_url) 
    c.setFillColorRGB(0, 0, 0)  # Black color

    c.setFont('Helvetica', 8) 
    c.drawString(20, 20, "verification url:")
     

    c.save()
 
    watermark = PdfReader(open(waterPath, "rb"))
    output_file = PdfWriter()
    input_file = PdfReader(open(real_doc_path, "rb"))
 
    page_count = len(input_file.pages) 
    for page_number in range(page_count): 
        input_page = input_file.pages[page_number]
        input_page.merge_page(watermark.pages[0]) 
        output_file.add_page(input_page)
 
    with open(output_doc_path, "wb") as outputStream:
        output_file.write(outputStream)
        outputStream.close()
  