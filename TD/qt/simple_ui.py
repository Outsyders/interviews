import time
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
)
from PySide6.QtCore import QObject, QThread, Signal, Slot



class Worker(QObject):
    finished = Signal(str) 

    def run_long_task(self):
        """Simulates a 5-second blocking pipeline process (e.g., publishing)."""
        print("Worker: Starting long task...")
        time.sleep(5) 
        print("Worker: Task finished.")
        self.finished.emit("Task Complete!")


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Non-Blocking Task Runner (PySide6)")
        self.setGeometry(100, 100, 400, 150)
        
        self.status_label = QLabel("Ready to run task...")
        self.start_button = QPushButton("Start 5s Task (Should Not Freeze)")
        self.start_button.clicked.connect(self.start_task)
        
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_task(self):
        """Initializes the worker and moves it to a new thread."""
        self.status_label.setText("Task running... (GUI should be responsive)")
        self.start_button.setEnabled(False)
        
        self.thread = QThread()
        self.worker = Worker()
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_long_task)
        self.worker.finished.connect(self.task_finished)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    @Slot(str)
    def task_finished(self, result_message: str):
        """Slot executed safely on the main thread after the worker is done."""
        self.status_label.setText(result_message)
        self.start_button.setEnabled(True)        
        print(f"Main Thread: UI updated with message: {result_message}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())