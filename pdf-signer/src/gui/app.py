from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QDesktopWidget
import os
from utils.pdf_signer import AddSignature
from utils.pdf_viewer import PDFViewer
from PyQt5.QtWidgets import QLineEdit
import platform
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Signer")

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Input field for signature text
        self.signature_input = QLineEdit(self)
        self.signature_input.setPlaceholderText("Enter your signature text here")
        self.layout.addWidget(self.signature_input)

        # Select file button
        self.select_file_button = QPushButton("Select PDF File", self)
        self.select_file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_file_button)

        # Sign button
        self.sign_button = QPushButton("Sign PDF", self)
        self.sign_button.clicked.connect(self.sign_pdf)
        self.layout.addWidget(self.sign_button)

        self.selected_file = None

    def select_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.selected_file = file_path

            # Create a new window for PDF preview
            self.preview_window = QWidget()
            self.preview_window.setWindowTitle("PDF Preview")

            # Get screen size and calculate window size
            screen = QDesktopWidget().screenGeometry()
            width = screen.width() * 2 // 4  # 2/4 of screen width
            height = screen.height() * 2 // 3  # 2/3 of screen height
            self.preview_window.resize(width, height)

            # Create a layout for the new window
            layout = QVBoxLayout(self.preview_window)

            # PDF Viewer
            self.pdf_viewer = PDFViewer(self.preview_window)
            self.pdf_viewer.load_pdf(file_path)
            layout.addWidget(self.pdf_viewer)

            # Buttons layout
            buttons_layout = QHBoxLayout()

            # Cancel button
            cancel_button = QPushButton("Close", self.preview_window)
            cancel_button.clicked.connect(self.preview_window.close)
            buttons_layout.addWidget(cancel_button)

            # Add buttons layout to the main layout
            layout.addLayout(buttons_layout)

            # Show the preview window
            self.preview_window.setLayout(layout)
            self.preview_window.show()


    def sign_pdf(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Warning", "Please select a PDF file first!")
            return

        signature_text = self.signature_input.text()
        if not signature_text:
            QMessageBox.warning(self, "Warning", "Please enter a signature text!")
            return

        # Pobieranie nowej pozycji podpisu z podglądu PDF
        x, y = self.pdf_viewer.get_signature_position()
        output_path = os.path.join(os.path.dirname(self.selected_file), f"signed_{os.path.basename(self.selected_file)}")

        # Call AddSignature
        AddSignature(self.selected_file, output_path, signature_text, x, y)
        QMessageBox.information(self, "Success", f"PDF signed successfully and saved as {output_path}")

        self.open_folder(os.path.dirname(output_path))

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # Mac
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])
