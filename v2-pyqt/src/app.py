import sys
import os

# from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QAction, QFileDialog, QProxyStyle
# import PyQt5.QtWidgets as qtw

import PyQt5.QtWidgets as pyqt
# print(pyqt.QStyleOptionTab.shape)

import settings
from editor import FileEditor
from viewer import Viewer
from browser import Browser

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

class VPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        # self.setPalette(settings.editor["palette"])
        # self.setFont(settings.editor["font"])
        # self.layout().setContentsMargins(0,0,0,0)

    def add(self, w):
        self.layout().addWidget(w)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings.init()

        self.setWindowTitle("tomino v2")
        self.resize(1200, 600)
        self.setPalette(settings.app["palette"])
        f = self.font()
        f.setPointSize(16)
        self.setFont(f)

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

        # self.editor_panel = VPanel(self)
        editor_layout = QVBoxLayout()
        self.file_editor = FileEditor()
        self.cursor_label = QLabel("BLA")
        editor_layout.addWidget(self.file_editor)
        editor_layout.addWidget(self.cursor_label)

        self.viewer = Viewer(self)

        browser_layout = QHBoxLayout()
        self.browser = Browser(self)
        browser_layout.addWidget(QLabel("a"), 1)
        browser_layout.addWidget(self.browser, 4)
        # self.browser_panel.layout().addChildLayout(hl)
        # self.browser_panel.add(self.browser)

        self.browser.load("/Users/mbruno/Physics/tomino/dummy")

        layout = QHBoxLayout(main)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addLayout(browser_layout, 20)
        layout.addLayout(editor_layout, 40)
        # layout.addLayout(viewer_layout, 40)

        self.setCentralWidget(main)


    def open(self):
        f = QFileDialog.getExistingDirectory(self, "Open folder ...", None, QFileDialog.ShowDirsOnly)
        if os.path.exists(f):
            self.browser.load(f)

    def settings(self):
        if self.settings_window is None:
            self.settings_window = settings.SettingsWindow()
        self.settings_window.show()

    def weak(self):
        if not self.main_tex_file is None:
            self.viewer.load()

app = QApplication(sys.argv)
# app.setStyle("Fusion")
# print(app.style().)

from PyQt5.QtCore import Qt

class Style(QProxyStyle):
    def drawControl(self, element, option, painter, widget):
        # if element == self.CE_TabBarTab:
        #     painter.drawText(option.rect, Qt.AlignLeft, option.text)
        #     return
        super(Style, self).drawControl(element, option, painter, widget)  
app.setStyle(Style(app.style()))

window = MainWindow()
window.show()

sys.exit(app.exec())