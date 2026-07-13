from PyQt6.QtGui import QFont, QFontDatabase, QColor, QPalette
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpinBox
from PyQt6.QtCore import Qt #, QFile, QIODevice

import os

app = {}
editor = {}
browser = {}
viewer = {}

themes = {
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
        "error": "#b9552e",
    }
}

def init():
    theme = get_theme()

    id = QFontDatabase.addApplicationFont(f'{os.path.dirname(__file__)}/assets/source-code-pro/SourceCodePro-Regular.ttf')
    families = QFontDatabase.applicationFontFamilies(id)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Highlight, QColor(theme['highlight']))
    palette.setColor(QPalette.ColorRole.Text, QColor(theme['text']))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(theme['text']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(theme['text']))
    palette.setColor(QPalette.ColorRole.Window, QColor(theme['app-background']))

    editor["tab"] = 4
    editor["font"] = QFont(families[0], 16)
    editor["palette"] = QPalette(palette)
    editor["palette"].setColor(QPalette.ColorRole.Base, QColor(theme['text-background']))

    font = QFont()
    font.setFamily(font.defaultFamily())
    font.setPointSize(16)

    app["palette"] = QPalette(palette)

    browser["palette"] = QPalette(palette)
    browser["palette"].setColor(QPalette.ColorRole.Base, QColor(theme['browser-background']))
    browser["palette"].setColor(QPalette.ColorRole.Window, QColor(theme['browser-background']))
    browser["palette"].setColor(QPalette.ColorRole.BrightText, QColor(theme['green']))
    browser["font"] = font

    viewer["palette"] = QPalette(palette)
    viewer["palette"].setColor(QPalette.ColorRole.Window, QColor(theme['text-background']))

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Highlight, QColor(theme['highlight']))
    palette.setColor(QPalette.ColorRole.Text, QColor(theme['gray']))
    palette.setColor(QPalette.ColorRole.Base, QColor(theme['text-background']))

    viewer["error"] = {
        "palette": palette,
        "font": font,
        }

    app["compiler"] = {
        'weak': 'latexmk -pdf -silent',
        'hard': 'latexmk -g -f -pdf -silent'
    }
    app["synctex"] = '-synctex=1'


def get_theme():
    return themes['dark']

class SpinBox(QWidget):
    def __init__(self, name, field, min):
        super().__init__()
        layout = QHBoxLayout()
        
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
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


