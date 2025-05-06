import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QToolButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QBrush, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QProcess

class RoundedPixmap(QPixmap):
    def __init__(self, pixmap, radius=12):
        super().__init__(pixmap)
        self.radius = radius

    def roundedPixmap(self):
        rounded = QPixmap(self.size())
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)
        painter.end()
        return rounded

class AppButton(QToolButton):
    def __init__(self, icon, text):
        super().__init__()
        self.setIcon(icon)
        self.setText(text)
        self.setIconSize(QSize(64, 64))
        self.setFixedSize(100, 100)
        self.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 5px;
                color: white;
                text-align: center;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 50);
                border-radius: 10px;
            }
        """)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

class AppLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lanzador de Aplicaciones")
        self.setFixedSize(1451, 640)  # 16:7 aspect ratio at 640p
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # Set background
        self.set_background()

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Left side (empty for now)
        left_widget = QWidget()
        main_layout.addWidget(left_widget, 1)

        # Right side (app grid)
        right_widget = QWidget()
        right_layout = QGridLayout()
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 2)

        # Load apps from database
        self.load_apps(right_layout)

    def set_background(self):
        background_path = os.path.join(os.path.dirname(__file__), "background.png")
        if os.path.exists(background_path):
            background = QPixmap(background_path)
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(background.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            print(f"Background image not found at {background_path}")

    def load_apps(self, layout):
        import sqlite3
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name, image_path, exec_path, comment FROM apps")
        apps = cursor.fetchall()
        conn.close()

        for i, app in enumerate(apps):
            name, image_path, exec_path, _ = app
            image_path = os.path.join(os.path.dirname(__file__), image_path)
            if os.path.exists(image_path):
                pixmap = RoundedPixmap(image_path)
                rounded_pixmap = pixmap.roundedPixmap()
                icon = QIcon(rounded_pixmap)
                button = AppButton(icon, name)
                button.clicked.connect(lambda _, path=exec_path: self.launch_app(path))
                row = i // 4
                col = i % 4
                layout.addWidget(button, row, col, Qt.AlignCenter)
            else:
                print(f"Image not found for {name} at {image_path}")

    def launch_app(self, path):
        if path.endswith('.exe'):
            QProcess.startDetached(path)
        elif path.endswith('.py'):
            QProcess.startDetached(sys.executable, [path])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = AppLauncher()
    launcher.show()
    sys.exit(app.exec_())