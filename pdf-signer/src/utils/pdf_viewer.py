from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint
import fitz

class PDFViewer(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.scaled_pixmap = None
        self.pdf_scale_factor = 1.0
        self.signature_label = QLabel("Your Signature", self)
        self.signature_label.setStyleSheet("background-color: yellow; border: 1px solid black;")
        self.signature_label.show()
        self.dragging = False  # Flaga przeciągania
        self.update_signature_position()  # Ustawienie domyślnej pozycji w prawym dolnym rogu

    def update_signature_position(self):
        """Aktualizuje domyślną pozycję podpisu w prawym dolnym rogu."""
        offset_x, offset_y, pixmap_width, pixmap_height = self.get_pixmap_rect()
        
        # Ustawienie podpisu w prawym dolnym rogu z niewielkim marginesem
        margin = 10
        default_x = offset_x + pixmap_width - self.signature_label.width() - margin
        default_y = offset_y + pixmap_height - self.signature_label.height() - margin
        self.signature_label.move(default_x, default_y)

    def load_pdf(self, file_path):
        """Load and display the first page of the PDF, scaled to fit the widget."""
        self.file_path = file_path
        pdf_document = fitz.open(file_path)
        first_page = pdf_document[0]
        pix = first_page.get_pixmap(dpi=100)
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        # Skalowanie PDF do okna podglądu
        self.scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(self.scaled_pixmap)
        self.signature_label.raise_()  # Upewnij się, że etykieta jest na wierzchu
        self.update_signature_position()  # Aktualizacja pozycji po załadowaniu PDF-a

    # def resizeEvent(self, event):
    #     """Dostosowanie podpisu przy zmianie rozmiaru okna."""
    #     super().resizeEvent(event)
    #     self.update_signature_position()

    def mousePressEvent(self, event):
        """Obsługa kliknięcia myszką na podpisie."""
        if self.signature_label.geometry().contains(event.pos()):
            self.dragging = True
            self.mouse_offset = event.pos() - self.signature_label.pos()

    def mouseMoveEvent(self, event):
        """Obsługa przeciągania podpisu."""
        if self.dragging:
            new_position = event.pos() - self.mouse_offset
            self.signature_label.move(new_position)

    def mouseReleaseEvent(self, event):
        """Zakończenie przeciągania."""
        self.dragging = False

    def get_pixmap_rect(self):
        """
        Zwraca prostokąt (x, y, width, height) określający pozycję wyświetlanego obrazu PDF
        wewnątrz widgetu, biorąc pod uwagę centrowanie.
        """
        if self.pixmap():
            label_width = self.width()
            label_height = self.height()
            pixmap_width = self.pixmap().width()
            pixmap_height = self.pixmap().height()
            offset_x = (label_width - pixmap_width) // 2
            offset_y = (label_height - pixmap_height) // 2
            return offset_x, offset_y, pixmap_width, pixmap_height
        else:
            return 0, 0, self.width(), self.height()

    def get_signature_position(self):
        """
        Przekształca współrzędne podpisu (w obrębie widgetu) na współrzędne PDF.
        Używa obszaru wyświetlanego obrazu PDF, a nie całego widgetu, 
        a także uwzględnia wymiary etykiety podpisu, aby jako punkt odniesienia wziąć jej środek.
        """
        pdf_width = 595   # np. szerokość strony A4
        pdf_height = 842  # np. wysokość strony A4

        offset_x, offset_y, pixmap_width, pixmap_height = self.get_pixmap_rect()
        label_pos = self.signature_label.pos()

        # Oblicz pozycję etykiety względem obszaru pixmapy
        relative_x = label_pos.x() - offset_x
        relative_y = label_pos.y() - offset_y

        scale_x = pdf_width / pixmap_width
        scale_y = pdf_height / pixmap_height

        # Dodaj połowę wymiarów etykiety, aby środek etykiety był punktem odniesienia
        # oraz odejmij korektę (np. 10 jednostek) aby przesunąć podpis w lewo
        korekta_x = 10
        pdf_x = (relative_x + self.signature_label.width() / 2 - korekta_x) * scale_x
        pdf_y = pdf_height - ((relative_y + self.signature_label.height() / 2) * scale_y)

        return pdf_x, pdf_y