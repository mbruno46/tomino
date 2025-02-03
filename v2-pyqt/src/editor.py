import os

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTabWidget, QWidget, QPlainTextEdit, QScrollArea, QHBoxLayout, QStackedWidget, QStyleOptionTab
from PyQt5.QtGui import QPainter, QColor, QFontMetricsF

from highligher import Highlighter
import settings
import style
import autocompleter

# TODO
# parser -> input for linked tex files
#  -> refs for refs
# parser_bib

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


    def __init__(self, parent = None):
        # self.app = app
        super().__init__(parent)
        # self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.setTabStopDistance(QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)
        self.setPalette(settings.editor["palette"])
        self.setFont(settings.editor["font"])        

        self.number_bar = self.NumberBar(self)                
        self.highlighter = Highlighter(self.document())
        self.completer = autocompleter. AutoCompleter(self)
        
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


        

class FileEditor(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        # settings.apply_stylesheet("editor", self)
        self.setStyleSheet(style.editor_style)
        self.setPalette(settings.editor["palette"])
        self.setFont(settings.editor["font"])
        self.setAutoFillBackground(True)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_file)

        self.files = []

    def load_file(self, filename):
        if not filename in self.files:
            e = Editor()
            with open(filename,'r') as f:
                e.setPlainText(f.read())
            self.addTab(e, os.path.basename(filename))
            self.files.append(filename)

    def close_file(self, idx):
        self.removeTab(idx)
        self.files.remove(self.files[idx])

