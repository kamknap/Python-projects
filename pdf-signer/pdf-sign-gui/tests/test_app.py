import unittest
from unittest.mock import patch, Mock
import os
import sys
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtTest import QTest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from gui.app import MainWindow

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Tworzymy tylko jedną instancję QApplication, aby uniknąć błędów PyQt5"""
        cls.app = QApplication([])

    def setUp(self):
        """Tworzenie nowego okna dla każdego testu"""
        self.window = MainWindow()

    def test_no_file_selected(self):
        """Test próby podpisania PDF bez wybranego pliku"""
        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            self.window.sign_pdf()
            mock_warning.assert_called_with(self.window, "Warning", "Please select a PDF file first!")

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', return_value=("test.pdf", "PDF Files (*.pdf)"))
    def test_file_selection(self, mock_get_open_file_name):
        """Test wyboru pliku PDF"""
        self.window.select_file()
        self.assertEqual(self.window.selected_file, "test.pdf")

    def test_empty_signature(self):
        """Test próby podpisania PDF bez wpisanej treści podpisu"""
        self.window.signature_input.setText('')
        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            self.window.sign_pdf()
            mock_warning.assert_called_with(self.window, "Warning", "Please enter a signature text!")

    @patch('utils.pdf_signer.AddSignature')
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_sign_pdf_success(self, mock_information, mock_add_signature):
        """Test poprawnego podpisania pliku PDF"""
        self.window.selected_file = "test.pdf"
        self.window.signature_input.setText("Test Signature")
        self.window.pdf_viewer = Mock()
        self.window.pdf_viewer.get_signature_position.return_value = (100, 200)

        self.window.sign_pdf()

        mock_add_signature.assert_called_with("test.pdf", "signed_test.pdf", "Test Signature", 100, 200)
        mock_information.assert_called_with(self.window, "Success", "PDF signed successfully and saved as signed_test.pdf")

    def test_close_preview_window(self):
        """Test zamykania okna podglądu PDF"""
        self.window.selected_file = "test.pdf"
        self.window.select_file()

        self.assertIsNotNone(self.window.preview_window)

        close_button = self.window.preview_window.findChild(QPushButton)
        self.assertIsNotNone(close_button)

        QTest.mouseClick(close_button, 1)

        self.assertFalse(self.window.preview_window.isVisible())

if __name__ == '__main__':
    unittest.main()
