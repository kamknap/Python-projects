import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 800, 600)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(pdf_path))
        
        self.setCentralWidget(self.browser)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer('file:///C:/Users/knapi/Desktop/Studia/fizyka/C3_Dynamika_cz.1_2022 AHK.pdf')
    viewer.show()
    sys.exit(app.exec_())