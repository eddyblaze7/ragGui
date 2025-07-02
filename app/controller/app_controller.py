# controller/app_controller.py

from PySide6.QtWidgets import QFileDialog
from model.app_model import AppModel
from view.main_window import MainWindow
from rag.querry_engine import QueryEngine
from pathlib import Path


class AppController:
    def __init__(self, model: AppModel, view: MainWindow):
        self.model = model
        self.view = view
        #self.engine = QueryEngine(model_path="models/llama-2.gguf")  # Path to your GGUF model
        self.engine = self.model.query_engine  # Use the model's query engine directly


        # Connect view events to controller methods
        self.view.load_button.clicked.connect(self.load_documents)
        self.view.query_button.clicked.connect(self.query_documents)

    def load_documents(self):
        data_folder = Path("data")
        file_paths = list(data_folder.glob("*.pdf")) + list(data_folder.glob("*.docx")) + list(data_folder.glob("*.txt"))

        if not file_paths:
            self.view.show_status("No documents found in the data folder.")
            return

        file_paths = [str(path) for path in file_paths]  # convert to strings
        # self.model.document_paths = file_paths
        # self.engine.index_documents(file_paths)
        self.model.load_and_index_documents(file_paths)
        self.view.show_status("Documents loaded and indexed from 'data/'.")
        
    def query_documents(self):
        query_text = self.view.query_input.toPlainText()
        if not query_text.strip():
            self.view.show_status("Please enter a query.")
            return

        self.view.show_status("Thinking...")
        answer = self.engine.query(query_text)
        self.view.show_answer(answer)
        self.view.show_status("Done.")
