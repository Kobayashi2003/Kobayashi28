import sys

from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QFileDialog, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QDragEnterEvent, QIcon

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag and Drop Example")
        self.resize(300, 200)
        self.QLable = QLabel(self)
        self.QLable.setGeometry(10, 10, 280, 100)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        self.QLable.setText("File Drag: " + a0.mimeData().text())
        a0.accept()

    def dropEvent(self, a0: QDragEnterEvent) -> None:
        self.QLable.setText("File Drop: " + a0.mimeData().text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
