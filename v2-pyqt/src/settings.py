from PyQt5.QtGui import QFont, QFontDatabase, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QSpinBox
from PyQt5.QtCore import Qt, QFile, QIODevice

# from PyQt5.QtGui import QIcon, QPixmap
# import glob, os
# icons = {}
# for f in glob.glob("icons/*"):
#     icons[os.path.basename(f)] = QIcon(QPixmap(f))

app = {}
editor = {}
browser = {}
viewer = {}

theme = {
    "dark": {
        "app-background": "#1c1f26",
        "text-background": "#232830",
        "browser-background": "#2b303b",
        "text": "#dfe1e8",
        "gray": "#717171",
        "hover": "#124670",
        "highlight": "#1f4b70",
        "border": "#333d46",
        "green": '#a6e86d',
        "command": "#82c448",
        "square": "#f1727f",
        "curly": "#ff84e8",
        "comment": "#5d90c4",
    }
}

def init():
    global editor

    id = QFontDatabase.addApplicationFont('/Users/mbruno/Physics/tomino/v2-pyqt/src/assets/source-code-pro/SourceCodePro-Regular.ttf')
    families = QFontDatabase.applicationFontFamilies(id)

    palette = QPalette()
    palette.setColor(QPalette.Highlight, QColor(theme['dark']['highlight']))
    palette.setColor(QPalette.Text, QColor(theme['dark']['text']))
    palette.setColor(QPalette.HighlightedText, QColor(theme['dark']['text']))
    palette.setColor(QPalette.WindowText, QColor(theme['dark']['text']))
    palette.setColor(QPalette.Window, QColor(theme['dark']['app-background']))

    editor["font"] = QFont(families[0], 16)
    editor["palette"] = QPalette(palette)
    editor["palette"].setColor(QPalette.Base, QColor(theme['dark']['text-background']))

    app["palette"] = QPalette(palette)

    browser["palette"] = QPalette(palette)
    browser["palette"].setColor(QPalette.Base, QColor(theme['dark']['browser-background']))
    browser["palette"].setColor(QPalette.BrightText, QColor(theme['dark']['green']))

    viewer["palette"] = QPalette(palette)
    viewer["palette"].setColor(QPalette.Window, QColor(theme['dark']['text-background']))

    app["compiler"] = {
        'weak': 'latexmk -pdf',
        'hard': 'latexmk -g -f -pdf'
    }

def apply_stylesheet(style, object):
    f = QFile(f':/assets/{style}.qss')
    f.open(QIODevice.ReadOnly)
    object.setStyleSheet(str(f.readAll(), 'utf-8'))
    f.close()

def get_theme():
    return theme['dark']

class SpinBox(QWidget):
    def __init__(self, name, field, min):
        super().__init__()
        layout = QHBoxLayout()
        
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        self.input = QSpinBox()
        self.input.setValue(field)
        self.input.setMinimum(min)
        layout.addWidget(self.input)
        self.setLayout(layout)

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        i1 = SpinBox("Font size", editor["font"].pointSize(), 8)
        
        layout.addWidget(i1)
        self.setLayout(layout)


