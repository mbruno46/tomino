from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit

from vpanel import VPanel
import settings

class Editor(QTextEdit):
    def __init__(self, app):
        self.app = app
        super().__init__()

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        # on macos CMD is ControlModifier
        if (e.modifiers() == Qt.ControlModifier):
            if e.key() == Qt.Key_R:
                print("cmd+R")
                self.app.viewer.load()

class EditorPanel(VPanel):
    def __init__(self, parent):
        super().__init__(parent)

        editor = Editor(parent)
        editor.setFont(settings.editor['font'])
        with open('test.tex','r') as f:
            editor.setText(f.read())
        self.layout.addWidget(editor)
