import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QFileDialog, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QGraphicsRectItem
from PySide6.QtGui import QPixmap, QImage, QPen, QColor
from PySide6.QtCore import Qt, QRectF
import fitz

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Open PDF button
        self.openButton = QPushButton("Open PDF")
        self.openButton.clicked.connect(self.OpenPdf)
        self.layout.addWidget(self.openButton)

        # Page navigation buttons
        self.navLayout = QHBoxLayout()
        self.prevButton = QPushButton("Previous Page")
        self.prevButton.clicked.connect(self.PrevPage)
        self.nextButton = QPushButton("Next Page")
        self.nextButton.clicked.connect(self.NextPage)
        self.navLayout.addWidget(self.prevButton)
        self.navLayout.addWidget(self.nextButton)
        self.layout.addLayout(self.navLayout)

        # Page viewer
        self.view = GraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)

        # PDF document and current page index
        self.doc = None
        self.currentPage = 0

    def OpenPdf(self):
        pdfPath, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if pdfPath:
            self.doc = fitz.open(pdfPath)
            self.currentPage = 0
            self.LoadPage()

    def LoadPage(self):
        if self.doc:
            page = self.doc[self.currentPage]
            pix = page.get_pixmap()
            qtImage = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qtImage)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            self.view.setScene(self.scene)
            self.view.setPdfPage(self.doc, self.currentPage)

    def NextPage(self):
        if self.doc and self.currentPage < len(self.doc) - 1:
            self.currentPage += 1
            self.LoadPage()

    def PrevPage(self):
        if self.doc and self.currentPage > 0:
            self.currentPage -= 1
            self.LoadPage()

class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.pdf_page = None
        self.current_page = 0
        self.startPos = None
        self.endPos = None

    def setPdfPage(self, doc, page_num):
        self.pdf_page = doc[page_num]
        self.current_page = page_num

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = self.mapToScene(event.pos())
            self.endPos = None

    def mouseMoveEvent(self, event):
        if self.startPos:
            self.endPos = self.mapToScene(event.pos())
            rect = QRectF(self.startPos, self.endPos)
            self.scene().clearSelection()
            self.scene().addRect(rect, QPen(QColor(255, 0, 0, 150)))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.startPos and self.endPos:
            text = self.extractTextFromRect(QRectF(self.startPos, self.endPos))
            print("Selected text:", text)
            self.startPos = None
            self.endPos = None

    def extractTextFromRect(self, rect):
        if self.pdf_page:
            x1, y1, x2, y2 = rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height()
            rect_coords = fitz.Rect(x1, y1, x2, y2)
            text = self.pdf_page.get_text("text", clip=rect_coords)
            return text
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())
