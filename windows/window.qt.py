from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton

class RoundedWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Eliminar los bordes
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: white; border-radius: 50px;")  # Esquinas redondeadas

        # Botón para cerrar la ventana
        close_button = QPushButton('X', self)
        close_button.setGeometry(360, 10, 30, 30)
        close_button.clicked.connect(self.close)

        # Para mover la ventana (arrastrando con el ratón)
        self.oldPos = self.pos()

    # Permitir mover la ventana arrastrando
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

app = QApplication([])
window = RoundedWindow()
window.show()
app.exec_()
