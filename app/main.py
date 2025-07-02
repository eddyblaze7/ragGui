# main.py

import sys
import os
# Add the root path to sys.path so it can find `rag` and `model`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from PySide6.QtWidgets import QApplication, QMessageBox

from model.app_model import AppModel
from view.main_window import MainWindow
from controller.app_controller import AppController
from pathlib import Path

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


def main():
    app = QApplication(sys.argv)

    try:
        model = AppModel()
        view = MainWindow()
        controller = AppController(model, view)

        view.show()
        sys.exit(app.exec())

    except Exception as e:
        logging.exception("Unhandled exception occurred during startup.")
        QMessageBox.critical(None, "Application Error", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
