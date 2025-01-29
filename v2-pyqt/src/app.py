import sys

# from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
# import PyQt5.QtWidgets as qtw

from editor import EditorPanel
from viewer import Viewer
from browser import Browser

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # button = QPushButton("Press Me!")
        # button.clicked.connect(lambda x: print('ciao'))
        # self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        layout = QHBoxLayout(self)
        
        self.editor = EditorPanel(self)
        self.viewer = Viewer(self)
        self.browser = Browser(self)

        layout.addWidget(self.browser(), 1)
        layout.addWidget(self.editor(),2)
        layout.addWidget(self.viewer(),2)
        
        main = QWidget()
        main.setLayout(layout)
        self.setCentralWidget(main)

    def clicked(self):
        print("Ciao")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()