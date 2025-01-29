from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QTextEdit, QFrame, QLabel, QWidget, QHBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QPainter, QColor, QFont

from vpanel import VPanel
from highligher import Highlighter
import settings

class Editor(QPlainTextEdit):

    class NumberBar(QWidget):
        def __init__(self, editor):
            super().__init__(editor)
            self.editor = editor

            width = self.fontMetrics().width("10000") + 10
            self.setFixedWidth(width)
            self.editor.setViewportMargins(width, 0, 0, 0)

            # self.editor.blockCountChanged.connect(self.updateWidth)
            self.editor.updateRequest.connect(self.updateContents) # triggered by resizing of editor
            self.font = QFont()

        def paintEvent(self, event):            
            painter = QPainter(self)
            painter.fillRect(event.rect(), settings.editor["palette"].base())
            
            block = self.editor.firstVisibleBlock()
 
            # Iterate over all visible text blocks in the document.
            while block.isValid():
                blockNumber = block.blockNumber()
                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
 
                # Check if the position of the block is out side of the visible area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break
 
                # We want the line number for the selected line to be bold.
                if blockNumber == self.editor.textCursor().blockNumber():
                    # self.font.setBold(True)
                    painter.setPen(settings.editor["palette"].text().color())
                else:
                    # self.font.setBold(False)
                    painter.setPen(QColor("#717171"))
                painter.setFont(self.font)
                
                # Draw the line number right justified at the position of the line.
                paint_rect = QRect(0, int(block_top), self.width(), self.editor.fontMetrics().height())
                painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber+1))
 
                block = block.next()
 
            painter.end()

            QWidget.paintEvent(self, event)

        def getWidth(self):
            count = self.editor.blockCount()
            width = self.fontMetrics().width(str(count)) + 10
            return width
        
        def updateWidth(self):
            width = self.getWidth()
            if self.width() != width:
                self.setFixedWidth(width)
                self.editor.setViewportMargins(width, 0, 0, 0)
        
        def updateContents(self, rect, scroll):
            print('hehre ', rect)
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
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.number_bar = self.NumberBar(self)
        # self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        # self.setLineWidth(2)

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        # on macos CMD is ControlModifier
        if (e.modifiers() == Qt.ControlModifier):
            if e.key() == Qt.Key_R:
                print("cmd+R")
                self.app.viewer.load()
        
        # if self.cursorPositionChanged():
        #     print("changed!!")

class EditorPanel(VPanel):
    def __init__(self, app):
        super().__init__()

        self.editor = Editor(app)
        self.editor.setFont(settings.editor['font'])

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

    def update_cursor_label(self, x, y):
        self.cursor_label.text = f"{x}, {y}"

    def load_file(self, filename):
        with open(filename,'r') as f:
            self.editor.setPlainText(f.read())
