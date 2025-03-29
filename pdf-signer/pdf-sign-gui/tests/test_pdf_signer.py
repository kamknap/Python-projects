import unittest
import sys, os
from PyPDF2 import PdfReader
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from utils.pdf_signer import AddSignature

class TestAddSignature(unittest.TestCase):

    def setUp(self):
        self.input_pdf = "test_input.pdf"
        self.output_pdf = "test_output.pdf"

        with open(self.input_pdf, "wb") as f:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from io import BytesIO
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(100, 750, "Test Page")
            can.save()
            f.write(packet.getvalue())

    def tearDown(self):
        if os.path.exists(self.input_pdf):
            os.remove(self.input_pdf)
        if os.path.exists(self.output_pdf):
            os.remove(self.output_pdf)

    def test_signature_addition(self):
        AddSignature(self.input_pdf, self.output_pdf, "Test Signature")
        self.assertTrue(os.path.exists(self.output_pdf))

    def test_output_pdf_valid(self):
        AddSignature(self.input_pdf, self.output_pdf, "Test Signature")
        reader = PdfReader(self.output_pdf)
        self.assertGreater(len(reader.pages), 0)

    def test_signature_position(self):
        AddSignature(self.input_pdf, self.output_pdf, "Test Signature", x=200, y=300)
        reader = PdfReader(self.output_pdf)
        page = reader.pages[0]
        
        text = page.extract_text()
        self.assertIn("Test Signature", text)

if __name__ == '__main__':
    unittest.main()