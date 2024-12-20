import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QFileDialog, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QImage
import fitz

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        #main layout
        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        #open PDF button
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

        #page viewer
        self.view = QGraphicsView()
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

    def NextPage(self):
        if self.doc and self.currentPage < len(self.doc) - 1:
            self.currentPage += 1
            self.LoadPage()

    def PrevPage(self):
        if self.doc and self.currentPage > 0:
            self.currentPage -= 1
            self.LoadPage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())