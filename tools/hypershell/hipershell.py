import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt

class HyperShell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("HyperShell")
        self.resize(800, 600)

        # Crear el área de texto para la consola
        self.console = QTextEdit(self)
        self.console.setFont(QFont("Courier New", 10))
        self.console.setStyleSheet("background-color: black; color: white;")
        self.console.setReadOnly(True)
        self.console.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.console.cursorPositionChanged.connect(self.handle_cursor_position)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.console)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Inicializar prompt
        self.current_directory = os.getcwd()
        self.prompt()

    def prompt(self):
        """Muestra el prompt con la ubicación actual."""
        self.console.append(f"{self.current_directory}> ")  # Prompt estilo consola
        self.console.moveCursor(QTextCursor.End)

    def handle_cursor_position(self):
        """Evitar que el cursor se mueva fuera de la línea actual."""
        cursor = self.console.textCursor()
        if cursor.blockNumber() < self.console.document().blockCount() - 1:
            self.console.moveCursor(QTextCursor.End)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            command = self.get_current_command()
            self.execute_command(command)
        elif event.key() == Qt.Key_Backspace:
            if self.is_cursor_in_prompt():
                event.ignore()  # Prevenir borrar el prompt
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def get_current_command(self):
        """Obtiene el comando que el usuario escribió después del prompt."""
        full_text = self.console.toPlainText().splitlines()
        if full_text:
            last_line = full_text[-1]
            return last_line.split("> ", 1)[-1].strip()  # Captura lo escrito tras el prompt
        return ""

    def is_cursor_in_prompt(self):
        """Verifica si el cursor está en la línea del prompt."""
        cursor = self.console.textCursor()
        prompt_pos = self.console.toPlainText().rfind(f"{self.current_directory}> ")
        return cursor.position() <= prompt_pos + len(f"{self.current_directory}> ")

    def execute_command(self, command):
        if command:
            if command.startswith("hypershell_"):  # Comando específico de HyperShell
                self.handle_hypershell_command(command)
            else:  # Ejecutar en PowerShell
                self.execute_powershell_command(command)
        self.prompt()

    def handle_hypershell_command(self, command):
        """Maneja comandos especiales de HyperShell."""
        if command == "hypershell_greet":
            self.console.append("Hello from HyperShell!")
        else:
            self.console.append(f"Unknown HyperShell command: {command}")

    def execute_powershell_command(self, command):
        """Ejecuta un comando en PowerShell."""
        try:
            # Ejecutar comando en PowerShell
            result = subprocess.run(
                ["powershell", "-Command", command], 
                capture_output=True, 
                text=True, 
                shell=True
            )
            # Mostrar salida o error
            if result.stdout:
                self.console.append(result.stdout)
            if result.stderr:
                self.console.append(f"Error: {result.stderr}")
        except Exception as e:
            self.console.append(f"Error executing PowerShell command: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shell = HyperShell()
    shell.show()
    sys.exit(app.exec_())
