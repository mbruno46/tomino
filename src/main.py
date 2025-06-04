import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QSplitter
from PyQt6.QtGui import QAction

import settings
import style
from editor import FileEditor, completer
from finder import Finder
from viewer import Viewer
from browser import Browser
from latex import Compiler

menus = {
    "&File": [
        ("&Open folder...", 'Ctrl+O', 'open'),
        ('separator', '', ''),
        ("&Prefs...", 'Ctrl+P', 'settings'),
        ('separator', '', ''),
        ('&Save', 'Ctrl+S', 'file_editor.save_file'),
        ('&Recompile TeX (weak)', 'Ctrl+R', 'weak'),
        ('&Recompile TeX (hard)', 'Ctrl+Shift+R', 'hard'),
        ('separator', '', ''),
        ("&Close", 'Ctrl+Q', 'close'),
    ],
    "&Edit": [
        ("&Undo", 'Ctrl+Z', 'file_editor.undo'),
        ("&Redo", 'Ctrl+Shift+Z', 'file_editor.redo'),
        ('separator', '', ''),
        ("&Cut", 'Ctrl+X', 'file_editor.cut'),
        ("&Copy", 'Ctrl+C', 'file_editor.copy'),
        ("&Paste", 'Ctrl+V', 'file_editor.paste'),
        ('separator', '', ''),
        ("&Find", 'Ctrl+F', 'finder.toggle'),
        ('separator', '', ''),
        ("&Toggle line comment", 'Ctrl+/', 'file_editor.comment'),
    ],
    "&View": [
        ("&Zoom In", 'Ctrl++', 'viewer.zoomin'),
        ("&Zoom Out", 'Ctrl+-', 'viewer.zoomout'),
        ("&Fit Width", 'Ctrl+W', 'viewer.fitW'),
        ("&Fit Height", 'Ctrl+Shift+W', 'viewer.fitH'),
        # ("&Invert colors", 'Ctrl+I', 'viewer.invert'),
        ('separator', '', ''),
        ("&Switch panel 1", 'Ctrl+1', 'file_editor.setCurrentIndex1'),
        ("&Switch panel 2", 'Ctrl+2', 'file_editor.setCurrentIndex2'),
        ("&Switch panel 3", 'Ctrl+3', 'file_editor.setCurrentIndex3'),
        ("&Switch panel 4", 'Ctrl+4', 'file_editor.setCurrentIndex4'),
        ('separator', '', ''),
        ("&Side Bar", 'Ctrl+B','toggle_browser_visibility'),
        ('separator', '', ''),
    ]
}

def get_nested_attr(obj, path):
    if '.' in path:
        s = path.split('.')
        return get_nested_attr(getattr(obj, s[0]), '.'.join(s[1:]))
    return getattr(obj, path)


class VPanel(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,4,0)
        self.layout().setSpacing(0)

    def add(self, w):
        self.layout().addWidget(w)


class MainWindow(QMainWindow):
    def __init__(self, debug):
        super().__init__()
        settings.init()

        self.setWindowTitle("tomino")
        self.resize(1200, 600)
        self.setPalette(settings.app["palette"])
        f = self.font()
        f.setPointSize(16)
        self.setFont(f)

        self.main_tex_file = None
        self.latex = None
        self.settings_window = None

        editor_panel = VPanel()
        self.file_editor = FileEditor()
        self.finder = Finder(self)
        editor_panel.add(self.file_editor)
        editor_panel.add(self.finder)
        
        self.viewer = Viewer(self)

        splitter = QSplitter()
        splitter.addWidget(editor_panel)
        splitter.addWidget(self.viewer)
        splitter.setStretchFactor(2, 2)
        splitter.setStyleSheet(style.splitter_style)
        
        self.browser = Browser(self)
        if debug:
            self.browser.load("/Users/mbruno/Physics/tomino/dummy")

        main = QWidget()

        layout = QHBoxLayout(main)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.browser, 20)
        layout.addWidget(splitter, 80)

        splitter.setSizes([(self.size().width() - self.browser.size().width())//2]*2)

        self.setCentralWidget(main)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        for m in menus:
            menu = menubar.addMenu(m)

            for tag, shortcut, func in menus[m]:
                if tag=='separator':
                    menu.addSeparator()
                    continue

                action = QAction(tag, self)
                action.setShortcut(shortcut)
                action.triggered.connect(get_nested_attr(self, func))
                menu.addAction(action)

    def open(self):
        f = QFileDialog.getExistingDirectory(self, "Open folder ...", None, QFileDialog.Option.ShowDirsOnly)
        if os.path.exists(f):
            completer.reset()
            self.browser.load(f)
            self.file_editor.close_all()
            self.viewer.close()

    def settings(self):
        if self.settings_window is None:
            self.settings_window = settings.SettingsWindow()
        self.settings_window.show()


    def recompile(self, weak):
        def inner(success):
            if not success:
                logfile = self.main_tex_file.replace('.tex', '.log')
                if os.path.isfile(logfile):
                    self.viewer.show_err(logfile)
            else:
                pdffile = self.main_tex_file.replace('.tex', '.pdf')
                if os.path.isfile(pdffile):
                    self.viewer.load(path = pdffile)

        if not self.main_tex_file is None:
            self.thread = Compiler(self.main_tex_file, weak)
            self.thread.success.connect(inner)
            self.thread.start()

    def weak(self):
        self.recompile(True)

    def hard(self):
        self.recompile(False)

    def toggle_browser_visibility(self):
        self.browser.toggle_visibility(int(self.width() * 0.20))
        self.browser.setFixedWidth(self.browser.width())

    def close(self):
        self.file_editor.close_all()
        self.viewer.close()
        super().close()

app = QApplication(sys.argv)
# app.setAttribute(Qt.AA_EnableHighDpiScaling, True) # maybe useful for QImage?
# app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

debug = False
if len(sys.argv)>1:
    debug = sys.argv[1]=='-d'

window = MainWindow(debug)
window.show()

pid = app.exec()
# useful to prevent strange seg fault
window.close()
sys.exit(pid)