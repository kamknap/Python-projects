def AddSignature(inputPdf, outputPdf, signatureText, x=None, y=None):
    import os
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO

    # Load the input PDF to get page dimensions
    existingPdf = PdfReader(inputPdf)
    first_page = existingPdf.pages[0]
    page_width = first_page.mediabox.width
    page_height = first_page.mediabox.height

    # Adjust coordinates based on actual page dimensions
    if x is None:
        x = page_width - 100  # Default to bottom-right corner
    if y is None:
        y = 50

    # Create empty PDF file with signature
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    can.drawString(x, y, signatureText)
    can.save()

    # Load signature
    packet.seek(0)
    newPdf = PdfReader(packet)
    output = PdfWriter()

    # Add signature to every page
    for pageNum, page in enumerate(existingPdf.pages):
        page.merge_page(newPdf.pages[0])
        output.add_page(page)

    with open(outputPdf, "wb") as fOut:
        output.write(fOut)