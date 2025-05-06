import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLabel, QToolButton, QPushButton, QDialog, 
                             QFormLayout, QSpinBox, QColorDialog, QLineEdit, QDialogButtonBox)
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QBrush, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, QSize, QProcess, QSettings

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
                border-color: rgba(255, 255, 255, 80)
            }
        """)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración")
        self.setFixedSize(350, 300)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton, QSpinBox {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4e6d8c;
            }
        """)
        
        layout = QFormLayout(self)
        
        self.button_size = QSpinBox()
        self.button_size.setRange(50, 200)
        self.button_size.setValue(100)
        layout.addRow("Tamaño de botones:", self.button_size)
        
        self.columns = QSpinBox()
        self.columns.setRange(1, 10)
        self.columns.setValue(4)
        layout.addRow("Número de columnas:", self.columns)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(12)
        layout.addRow("Tamaño de letra:", self.font_size)
        
        self.window_height = QSpinBox()
        self.window_height.setRange(480, 1080)
        self.window_height.setValue(640)
        self.window_height.setSingleStep(10)
        layout.addRow("Altura de la ventana:", self.window_height)
        
        self.accent_color = QPushButton("Seleccionar")
        self.accent_color.clicked.connect(self.choose_color)
        layout.addRow("Color de acento:", self.accent_color)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.accent_color.setStyleSheet(f"background-color: {color.name()};")

class AppLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lanzador de Aplicaciones")
        self.settings = QSettings("MiCompania", "AppLauncher")
        self.accent_color = self.settings.value("accent_color", "#3498db")
        self.window_height = self.settings.value("window_height", 640, type=int)
        self.update_window_size()

        # Set background
        self.set_background()

        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Apps grid
        apps_widget = QWidget()
        self.apps_layout = QGridLayout()
        apps_widget.setLayout(self.apps_layout)
        main_layout.addWidget(apps_widget)

        # Bottom menu
        bottom_menu = QWidget()
        bottom_menu.setFixedHeight(70)  # Reduced height
        bottom_menu.setStyleSheet(f"""
            background-color: rgba(0, 0, 0, 150);
            border-radius: 10px;
            margin: 10px;
        """)
        bottom_layout = QHBoxLayout()
        bottom_menu.setLayout(bottom_layout)
        
        config_button = QPushButton("Configuración")
        config_button.setFixedSize(120, 50)  # Adjusted size
        config_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: 2px solid {self.accent_color};
                border-radius: 5px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.accent_color};
            }}
        """)
        config_button.clicked.connect(self.open_config)
        bottom_layout.addWidget(config_button, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(bottom_menu, alignment=Qt.AlignCenter)

# Copiar para añadir otro boton
#        config_button = QPushButton("Configuración")
#        config_button.setFixedSize(120, 50)  # Adjusted size
#        config_button.setStyleSheet(f"""
#            QPushButton {{
#                background-color: transparent;
#                color: white;
#                border: 2px solid {self.accent_color};
#                border-radius: 5px;
#                padding: 5px;
#            }}
#            QPushButton:hover {{
#                background-color: {self.accent_color};
#            }}
#        """)
#        config_button.clicked.connect(self.open_config)
#        bottom_layout.addWidget(config_button, alignment=Qt.AlignCenter)

        # Load apps from database
        self.load_apps()

    def update_window_size(self):
        aspect_ratio = 16/7
        width = int(self.window_height * aspect_ratio)
        self.setFixedSize(width, self.window_height)

    def set_background(self):
        background_path = os.path.join(os.path.dirname(__file__), "background.png")
        if os.path.exists(background_path):
            background = QPixmap(background_path)
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(background.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            print(f"Background image not found at {background_path}")

    def load_apps(self):
        import sqlite3
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name, image_path, exec_path, comment FROM apps")
        apps = cursor.fetchall()
        conn.close()

        columns = self.settings.value("columns", 4, type=int)
        button_size = self.settings.value("button_size", 100, type=int)
        font_size = self.settings.value("font_size", 12, type=int)

        for i, app in enumerate(apps):
            name, image_path, exec_path, _ = app
            image_path = os.path.join(os.path.dirname(__file__), image_path)
            if os.path.exists(image_path):
                pixmap = RoundedPixmap(image_path)
                rounded_pixmap = pixmap.roundedPixmap()
                icon = QIcon(rounded_pixmap)
                button = AppButton(icon, name)
                button.setFixedSize(button_size, button_size)
                button.setFont(QFont("Arial", font_size))
                button.clicked.connect(lambda _, path=exec_path: self.launch_app(path))
                row = i % columns
                col = i // columns
                self.apps_layout.addWidget(button, row, col, Qt.AlignLeft | Qt.AlignTop)
            else:
                print(f"Image not found for {name} at {image_path}")

    def launch_app(self, path):
        if path.endswith('.exe'):
            QProcess.startDetached(path)
        elif path.endswith('.py'):
            QProcess.startDetached(sys.executable, [path])

    def open_config(self):
        dialog = ConfigDialog(self)
        dialog.button_size.setValue(self.settings.value("button_size", 100, type=int))
        dialog.columns.setValue(self.settings.value("columns", 4, type=int))
        dialog.font_size.setValue(self.settings.value("font_size", 12, type=int))
        dialog.window_height.setValue(self.window_height)
        dialog.accent_color.setStyleSheet(f"background-color: {self.accent_color};")
        
        if dialog.exec_():
            self.settings.setValue("button_size", dialog.button_size.value())
            self.settings.setValue("columns", dialog.columns.value())
            self.settings.setValue("font_size", dialog.font_size.value())
            self.settings.setValue("window_height", dialog.window_height.value())
            self.settings.setValue("accent_color", dialog.accent_color.styleSheet().split(":")[1].strip(";"))
            
            self.accent_color = self.settings.value("accent_color")
            self.window_height = dialog.window_height.value()
            self.update_window_size()
            
            # Clear and reload apps
            for i in reversed(range(self.apps_layout.count())): 
                self.apps_layout.itemAt(i).widget().setParent(None)
            self.load_apps()
            
            # Update config button style
            self.findChild(QPushButton, "").setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: white;
                    border: 2px solid {self.accent_color};
                    border-radius: 5px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {self.accent_color};
                }}
            """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = AppLauncher()
    launcher.show()
    sys.exit(app.exec_())