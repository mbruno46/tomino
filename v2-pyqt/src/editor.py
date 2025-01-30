from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QTextEdit, QFrame, QLabel, QWidget, QHBoxLayout, QPlainTextEdit, QMenu, QCompleter
from PyQt5.QtGui import QPainter, QColor, QFont, QTextCursor

from vpanel import VPanel
from highligher import Highlighter
import settings
import autocompleter


class Editor(QPlainTextEdit):

    class NumberBar(QWidget):
        def __init__(self, editor):
            super().__init__(editor)
            self.editor = editor

            width = self.fontMetrics().width("10000") + 10
            self.setFixedWidth(width)
            self.editor.setViewportMargins(width, 0, 0, 0)

            self.editor.updateRequest.connect(self.updateContents) 

        def paintEvent(self, event):            
            painter = QPainter(self)
            painter.fillRect(event.rect(), settings.editor["palette"].base())
            
            # block is basically a line
            block = self.editor.firstVisibleBlock()

            while block.isValid():
                blockNumber = block.blockNumber()
                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
 
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break
 
                if blockNumber == self.editor.textCursor().blockNumber():
                    painter.setPen(settings.editor["palette"].text().color())
                else:
                    painter.setPen(QColor("#717171"))
                painter.setFont(settings.editor["font"])
                
                # draw line number
                paint_rect = QRect(0, int(block_top), self.width(), self.editor.fontMetrics().height())
                painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber+1))
 
                block = block.next()
 
            painter.end()

            QWidget.paintEvent(self, event)

        # def getWidth(self):
        #     count = self.editor.blockCount()
        #     width = self.fontMetrics().width(str(count)) + 10
        #     return width
        
        # def updateWidth(self):
        #     width = self.getWidth()
        #     if self.width() != width:
        #         self.setFixedWidth(width)
        #         self.editor.setViewportMargins(width, 0, 0, 0)
        
        def updateContents(self, rect, scroll):
            self.setFixedHeight(self.editor.height())
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update(0, rect.y(), self.width(), rect.height())
            
            # if rect.contains(self.editor.viewport().rect()):   
                # fontSize = self.editor.currentCharFormat().font().pointSize()
                # self.font.setPointSize(fontSize)
                # self.font.setStyle(QFont.StyleNormal)
                # self.updateWidth()


    def __init__(self, app):
        self.app = app
        super().__init__()
        self.setPalette(settings.editor["palette"])
        # self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setFont(settings.editor["font"])
        
        self.number_bar = self.NumberBar(self)
        # self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        # self.setLineWidth(2)

        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.launch_autocomplention)
        self.completer = autocompleter.AutoCompleter(self)
        # self.textChanged.connect(self.completer.check_and_launch)

    def keyPressEvent(self, event):
        if self.completer.isVisible() and event.key() in [
            Qt.Key.Key_Enter,
            Qt.Key.Key_Return,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
            Qt.Key.Key_Tab,
            Qt.Key.Key_Backtab,
        ]:
            event.ignore()
            return
        super().keyPressEvent(event)
        self.completer.check_and_launch()

        # super().keyPressEvent(e)
        # # on macos CMD is ControlModifier
        # if (e.modifiers() == Qt.ControlModifier):
        #     if e.key() == Qt.Key_R:
        #         print("cmd+R")
        #         # self.app.viewer.load()
        
        # if self.cursorPositionChanged():
        #     print("changed!!")
        

    # def autocomplete(self, choice):
    #     tc = self.textCursor()
    #     word = self.current_word
    #     tc.insertText(choice[len(word):])
    #     self.setTextCursor(tc)


class EditorPanel(VPanel):
    def __init__(self, app):
        super().__init__()

        self.editor = Editor(app)
        # self.load_settings()
        self.highlighter = Highlighter(self.editor.document())

        self.cursor_label = QLabel()
        # self.line_numbers = LineNumbers(self.editor)

        # layoutH = QHBoxLayout()
        # layoutH.setSpacing(2)
        # layoutH.addWidget(self.line_numbers)
        # layoutH.addWidget(self.editor)
        
        # w = QWidget()
        # w.setLayout(layoutH)
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.cursor_label)

    # def load_settings(self):
        # self.editor.setFont(settings.editor['font'])

    def update_cursor_label(self, x, y):
        self.cursor_label.text = f"{x}, {y}"

    def clear(self):
        self.editor.setPlainText("")

    def load_file(self, filename):
        with open(filename,'r') as f:
            self.editor.setPlainText(f.read())
