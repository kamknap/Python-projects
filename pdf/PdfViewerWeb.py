import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        # Tworzenie widoku WebEngineView
        self.web_view = QWebEngineView()
        
        # Tworzenie przycisku "Open PDF"
        self.openButton = QPushButton("Open PDF")
        self.openButton.clicked.connect(self.open_pdf)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.openButton)
        layout.addWidget(self.web_view)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_pdf(self):
        pdf_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if pdf_path:
            print(f"Selected PDF path: {pdf_path}")  # Debugging line
            self.load_pdf(pdf_path)

    def load_pdf(self, pdf_path):
        self.web_view.setUrl(f"file:///{pdf_path}")
        print(f"Loading PDF: file:///{pdf_path}")  # Debugging line

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())