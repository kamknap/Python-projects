import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from utils.pdf_viewer import PDFViewer

app = QApplication([])

class TestPDFViewer(unittest.TestCase):

    def setUp(self):
        self.viewer = PDFViewer()

    def test_load_pdf(self):
        with patch('fitz.open') as mock_fitz:
            mock_pdf = mock_fitz.return_value
            mock_pdf.__getitem__.return_value.get_pixmap.return_value.samples = b'\x00' * (100 * 100 * 3)
            mock_pdf.__getitem__.return_value.get_pixmap.return_value.width = 100
            mock_pdf.__getitem__.return_value.get_pixmap.return_value.height = 100
            mock_pdf.__getitem__.return_value.get_pixmap.return_value.stride = 300

            self.viewer.load_pdf("test.pdf")
            self.assertIsNotNone(self.viewer.scaled_pixmap)

    def test_signature_position_initial(self):
        self.viewer.resize(800, 600)
        self.viewer.update_signature_position()

        offset_x, offset_y, width, height = self.viewer.get_pixmap_rect()
        margin = 10
        expected_x = offset_x + width - self.viewer.signature_label.width() - margin
        expected_y = offset_y + height - self.viewer.signature_label.height() - margin
        
        self.assertEqual(self.viewer.signature_label.x(), expected_x)
        self.assertEqual(self.viewer.signature_label.y(), expected_y)

    def test_drag_signature(self):
        start_pos = self.viewer.signature_label.pos()
        new_pos = QPoint(start_pos.x() + 50, start_pos.y() + 30)

        press_event = QMouseEvent(QMouseEvent.MouseButtonPress, start_pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        self.viewer.mousePressEvent(press_event)

        move_event = QMouseEvent(QMouseEvent.MouseMove, new_pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        self.viewer.mouseMoveEvent(move_event)

        release_event = QMouseEvent(QMouseEvent.MouseButtonRelease, new_pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        self.viewer.mouseReleaseEvent(release_event)

        self.assertNotEqual(self.viewer.signature_label.pos(), start_pos)

    def test_get_signature_position(self):
        self.viewer.resize(800, 600)
        self.viewer.update_signature_position()

        pdf_x, pdf_y = self.viewer.get_signature_position()
        
        self.assertGreater(pdf_x, 0)
        self.assertGreater(pdf_y, 0)


if __name__ == '__main__':
    unittest.main()
