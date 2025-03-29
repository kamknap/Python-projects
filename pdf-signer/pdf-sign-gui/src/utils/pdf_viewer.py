from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz

class PDFViewer(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.scaled_pixmap = None
        self.pdf_scale_factor = 1.0

    def load_pdf(self, file_path):
        """Load and display the first page of the PDF, scaled to fit the widget."""
        self.file_path = file_path  # Zapisz ścieżkę pliku PDF
        pdf_document = fitz.open(file_path)
        first_page = pdf_document[0]
        pix = first_page.get_pixmap(dpi=100)
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        # Scale the pixmap to 800x600
        self.scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(self.scaled_pixmap)

    def update_scaled_pixmap(self):
        """Scale the pixmap to fit the widget size."""
        if self.scaled_pixmap:
            self.pdf_scale_factor = min(self.width() / self.scaled_pixmap.width(), self.height() / self.scaled_pixmap.height())
            scaled_pixmap = self.scaled_pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """Handle widget resizing to update the scaled pixmap."""
        self.update_scaled_pixmap()