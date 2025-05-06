import sys
from PyQt6.QtWidgets import QApplication
from app.gui.main_window import MainWindow
from app.db.init_db import init_db

if __name__ == "__main__":
    init_db() # Khoi tao database
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())