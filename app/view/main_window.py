from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QHBoxLayout
)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline RAG Assistant")
        self.resize(900, 600)

        self.apply_dark_theme()

        # Main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Query input (1/3 of total height)
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("Enter your query here...")
        main_layout.addWidget(self.query_input, 1)

        # Output display (2/3 of total height)
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        main_layout.addWidget(self.output_display, 2)

        # Buttons
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load Documents")
        self.query_button = QPushButton("Query")

        self.load_button.setStyleSheet(self.button_style())
        self.query_button.setStyleSheet(self.button_style())

        button_layout.addStretch()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.query_button)

        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_status(self, message: str):
        self.status_label.setText(message)

    def show_answer(self, answer: str):
        self.output_display.append(f"\n→ {answer}")

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(70, 130, 180))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

    def button_style(self):
        return """

        QMainWindow {
        background-color: #2b2b2b;
        color: #ffffff;
        font-family: "Segoe UI", sans-serif;
    }
           QPushButton {
            background-color: #3c3f41;
            border: 1px solid #5c5f61;
            padding: 6px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #505354;
        }
        QTextEdit {
            background-color: #2b2b2b;
            color: white;
            border: 1px solid #5c5f61;
            font-family: "Segoe UI", sans-serif;
        """
