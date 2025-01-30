import sys
import os

# from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QAction, QFileDialog
# import PyQt5.QtWidgets as qtw

import settings
from editor import EditorPanel
from viewer import Viewer
from browser import BrowserPanel

menus = {
    "&File": [
        ("&Open folder...", 'Ctrl+O', 'open'),
        ('separator', '', ''),
        ("&Prefs...", 'Ctrl+P', 'settings'),
        ('separator', '', ''),
        ('&Recompile TeX (weak)', 'Ctrl+S', 'weak'),
        ('separator', '', ''),
        ("&Close", 'Ctrl+Q', 'close'),
    ]
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings.init()

        self.setWindowTitle("tomino v2")
        self.resize(1200, 600)
        self.setPalette(settings.app["palette"])

        self.main_tex_file = None
        self.settings_window = None

        menubar = self.menuBar()
        for m in menus:
            menu = menubar.addMenu(m)

            for tag, shortcut, func in menus[m]:
                if tag=='separator':
                    menu.addSeparator()
                    continue

                action = QAction(tag, self)
                action.setShortcut(shortcut)
                action.triggered.connect(getattr(self, func))
                menu.addAction(action)

        main = QWidget()

        self.editor = EditorPanel(self)
        self.viewer = Viewer(self)
        self.browser = BrowserPanel(self)

        layout = QHBoxLayout(main)
        layout.addWidget(self.browser(), 1)
        layout.addWidget(self.editor(),2)
        layout.addWidget(self.viewer(),2)

        self.setCentralWidget(main)


    def open(self):
        f = QFileDialog.getExistingDirectory(self, "Open folder ...", None, QFileDialog.ShowDirsOnly)
        if os.path.exists(f):
            self.browser.open_folder(f)

    def settings(self):
        if self.settings_window is None:
            self.settings_window = settings.SettingsWindow()
        self.settings_window.show()

    def weak(self):
        if not self.main_tex_file is None:
            self.viewer.load()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())