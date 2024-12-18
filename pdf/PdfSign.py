import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def AddSignature(inputPdf, outputPdf, signatureText, x=None, y=None):
    #create empty pdf file with signature
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Get page width and height
    page_width, page_height = letter
    
    # Set default position to bottom right if x and y are not provided
    if x is None:
        x = page_width - 100  # Adjust as needed
    if y is None:
        y = 50  # Adjust as needed

    can.drawString(x, y, signatureText)
    can.save()

    #load signature
    packet.seek(0)
    newPdf = PdfReader(packet)

    existingPdf = PdfReader(inputPdf)
    output = PdfWriter()

    #add signature on every page
    for pageNum in range(len(existingPdf.pages)):
        page = existingPdf.pages[pageNum]
        page.merge_page(newPdf.pages[0])
        output.add_page(page)

    with open(outputPdf, "wb") as fOut:
        output.write(fOut)

inputFolder = r"path"
outputFolder = r"path"
signatureText = "Jan Kowalski"

for fileName in os.listdir(inputFolder):
    if fileName.endswith(".pdf"):
        input_path = os.path.join(inputFolder, fileName)
        output_path = os.path.join(outputFolder, f"signed_{fileName}")
        AddSignature(input_path, output_path, signatureText)
        print(f"Podpisano: {fileName}")