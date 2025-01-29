import sys

# from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
# import PyQt5.QtWidgets as qtw

import settings
from editor import EditorPanel
from viewer import Viewer
from browser import BrowserPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings.init()

        self.setWindowTitle("tomino v2")
        self.resize(1200, 600)
        self.setPalette(settings.app["palette"])

        main = QWidget()

        # button = QPushButton("Press Me!")
        # button.clicked.connect(lambda x: print('ciao'))
        # self.setFixedSize(QSize(400, 300))
        self.editor = EditorPanel(self)
        self.viewer = Viewer(self)
        self.browser = BrowserPanel(self)

        layout = QHBoxLayout(main)
        layout.addWidget(self.browser(), 1)
        layout.addWidget(self.editor(),2)
        layout.addWidget(self.viewer(),2)

        self.setCentralWidget(main)

        # menubar = self.menuBar()
        # file_menu = menubar.addMenu("&File")
        # self.exit_action = file_menu.addAction("E&xit")
        # self.exit_action.setShortcut("Ctrl+Q")
        # self.exit_action.triggered.connect(self.close)


    # def clicked(self):
    #     print("Ciao")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())