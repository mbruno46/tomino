import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QAction, QFileDialog, QProxyStyle
# import PyQt5.QtWidgets as qtw

import PyQt5.QtWidgets as pyqt
# print(pyqt.QStyleOptionTab.shape)

import settings
from editor import FileEditor
from finder import Finder
from viewer import Viewer
from browser import Browser
from latex import build_pdf

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
        ("&Toggle line comment", 'Ctrl+/', 'file_editor.comment'),
    ],
    "&View": [
        ("&Zoom In", 'Ctrl++', 'viewer.zoomin'),
        ("&Zoom Out", 'Ctrl+-', 'viewer.zoomout'),
        ("&Fit Width", 'Ctrl+W', 'viewer.fitW'),
        ("&Fit Height", 'Ctrl+Shift+W', 'viewer.fitH'),
        ('separator', '', ''),
        ("&Find", 'Ctrl+F', 'finder.toggle'),
        ('separator', '', ''),
        ("&Invert colors", 'Ctrl+I', 'viewer.invert'),
    ]
}

def get_nested_attr(obj, path):
    if '.' in path:
        s = path.split('.')
        return get_nested_attr(getattr(obj, s[0]), '.'.join(s[1:]))
    return getattr(obj, path)


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

        main = QWidget()

        # self.editor_panel = VPanel(self)
        editor_layout = QVBoxLayout()
        self.file_editor = FileEditor()
        self.finder = Finder(self)
        editor_layout.addWidget(self.file_editor)
        editor_layout.addWidget(self.finder)

        self.viewer = Viewer(self)

        browser_layout = QHBoxLayout()
        # self.toolbar = ToolBar([('refresh', lambda x: print('ciao'))])
        self.browser = Browser(self)
        # browser_layout.addWidget(self.toolbar, 1)
        browser_layout.addWidget(self.browser, 4)
        # self.browser_panel.layout().addChildLayout(hl)
        # self.browser_panel.add(self.browser)

        # /Users/mbruno/Physics/ToM/dummy/
        self.browser.load("/Users/mbruno/Physics/ToM/dummy")

        layout = QHBoxLayout(main)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addLayout(browser_layout, 20)
        layout.addLayout(editor_layout, 40)
        layout.addWidget(self.viewer, 40)

        self.setCentralWidget(main)

        menubar = self.menuBar()
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
        f = QFileDialog.getExistingDirectory(self, "Open folder ...", None, QFileDialog.ShowDirsOnly)
        if os.path.exists(f):
            self.browser.load(f)

    def settings(self):
        if self.settings_window is None:
            self.settings_window = settings.SettingsWindow()
        self.settings_window.show()


    def recompile(self, weak):
        if not self.main_tex_file is None:
            build_pdf(self.main_tex_file, weak)
            self.viewer.load(path = self.main_tex_file.replace('.tex', '.pdf'))
    
    def weak(self):
        self.recompile(True)

    def hard(self):
        self.recompile(False)


app = QApplication(sys.argv)
app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
# f = QFile(':/assets/style.qss')
# f.open(QIODevice.ReadOnly)
# app.setStyleSheet(str(f.readAll(), 'utf-8'))
# f.close()

# f = QFile(':/assets/style.qss')
#         f.open(QIODevice.ReadOnly)
#         self.setStyleSheet(str(f.readAll(), 'utf-8'))
#         f.close()

# app.setStyle("Fusion")
# print(app.style().)

# from PyQt5.QtCore import Qt

# class Style(QProxyStyle):
#     def drawControl(self, element, option, painter, widget):
#         # if element == self.CE_TabBarTab:
#         #     painter.drawText(option.rect, Qt.AlignLeft, option.text)
#         #     return
#         super(Style, self).drawControl(element, option, painter, widget)  
# app.setStyle(Style(app.style()))

window = MainWindow()
window.show()

sys.exit(app.exec())