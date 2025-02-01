import os

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTabWidget, QWidget, QPlainTextEdit, QScrollArea, QHBoxLayout, QStackedWidget, QStyleOptionTab
from PyQt5.QtGui import QPainter, QColor, QFontMetricsF

from highligher import Highlighter
import settings
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

class FileEditor3(QWidget):
    class Tab(QWidget):
        def __init__(self, name):
            super().__init__()
            self.setLayout(QHBoxLayout())
            self.layout().addWidget(QLabel(name))
            btn = QPushButton("X")
            # self.closeRequest = btn.clicked
            self.layout().addWidget(btn)

    def __init__(self, parent = None):
        super().__init__(parent)
        # self.bar = QHBoxLayout()
        self.setLayout(QVBoxLayout())
        # self.tbar = self.Bar(self)
        scroll = QScrollArea(widgetResizable=True)
        scroll.setWidget(self.tbar)
        
        self.layout().addWidget(scroll)
        self.tabs = QStackedWidget()
        self.layout().addWidget(self.tabs)

        self.files = []

    def load_file(self, filename):
        if not filename in self.files:
            e = Editor()
            with open(filename,'r') as f:
                e.setPlainText(f.read())
            # self.tabs.addTab(e, os.path.basename(filename))
            self.tbar.addTab(os.path.basename(filename))
            self.tabs.addWidget(e)
            self.files.append(filename)
        

class FileEditor(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        # qs = QStyleOptionTab()
        # qs.TabFeatures()
        # self.setStyleSheet("""
        # QTabWidget::pane {
        # border: 1px solid;
        # }
        # """)
        self.setPalette(settings.editor["palette"])
        self.setFont(settings.editor["font"])
        # self.
        # self.setStyleSheet("""
        #     QTabBar::tab {
        #     border: 2px solid #C4C4C3;
        #     border-bottom-color: #C2C7CB; /* same as the pane color */
        #     border-top-left-radius: 4px;
        #     border-top-right-radius: 4px;
        #     min-width: 8ex;
        #     padding: 2px;
        #     }""")
        self.files = []

    def load_file(self, filename):
        if not filename in self.files:
            e = Editor()
            with open(filename,'r') as f:
                e.setPlainText(f.read())
            self.addTab(e, os.path.basename(filename))
            # self.tbar.addTab(os.path.basename(filename))
            # self.tabs.addWidget(e)
            self.files.append(filename)

class EditorPanel(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)


        self.file_editor = FileEditor(self)
        # self.tabs.setTabsClosable(True)
        # self.tabs.setAutoFillBackground(True)

        # tbar = self.tabs.tabBar()
        # tbar.setStyle
        # tbar.setAutoFillBackground(True)
        # tbar.setPalette(settings.editor["palette"])

        # self.tabs.tabCloseRequested.connect(self.close_file)
        self.files = []

        self.cursor_label = QLabel("BLA")

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.file_editor)
        self.layout().addWidget(self.cursor_label)

    def clear(self):
        pass
        # self.tabs.clear()

    def load_file(self, filename):
        # self.file_editor.load_file(filename)
        
        if not filename in self.files:
            e = Editor()
            with open(filename,'r') as f:
                e.setPlainText(f.read())
            self.file_editor.addTab(e, os.path.basename(filename))
            self.files.append(filename)
        idx = self.files.index(filename)
        # self.tabs.setCurrentIndex(idx)

    def close_file(self, idx):
        self.tabs.removeTab(idx)
        self.files.remove(self.files[idx])
