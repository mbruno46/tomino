import os

from PyQt5.QtCore import Qt, QRect, QFileSystemWatcher
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTabWidget, QWidget, QPlainTextEdit, QScrollArea, QHBoxLayout, QStackedWidget, QStyleOptionTab
from PyQt5.QtGui import QPainter, QColor, QFontMetricsF, QKeyEvent, QTextCursor, QTextDocument

from highligher import Highlighter
import settings
import style
from autocompleter import AutoCompleter

# TODO
# parser -> input for linked tex files
#  -> refs for refs
# parser_bib

completer = AutoCompleter()

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
        
        def updateContents(self, rect, scroll):
            self.setFixedHeight(self.editor.height())
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update(0, rect.y(), self.width(), rect.height())
            

    def __init__(self, parent = None, filename = None):
        # self.app = app
        super().__init__(parent)
        with open(filename,'r') as f:
            self.setPlainText(f.read())
        self.filename = filename
 
        # self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setTabStopDistance(QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)
        self.setPalette(settings.editor["palette"])
        self.setFont(settings.editor["font"])        

        self.number_bar = self.NumberBar(self)                
        self.highlighter = Highlighter(self.document())
        
        # self.textChanged.connect(parent.text_changed)
        

    def keyPressEvent(self, event: QKeyEvent):
        if completer.isVisible() and event.key() in [
            Qt.Key.Key_Enter,
            Qt.Key.Key_Return,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
            Qt.Key.Key_Tab,
            Qt.Key.Key_Backtab,
        ]:
            event.ignore()
            return
        # if event.modifiers() & Qt.KeyboardModifier.MetaModifier:
        #     if event.key() == Qt.Key.Key_Slash:
        #         self.comment_selection()
        #         return
        super().keyPressEvent(event)
        completer.check_and_launch()

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

    def comment(self):
        tc = self.textCursor()

        if tc.hasSelection():
            start, end = tc.selectionStart(), tc.selectionEnd()
            tc.setPosition(start)
            l0 = tc.blockNumber()
            tc.setPosition(end)
            l1 = tc.blockNumber()
        else:
            l0 = l1 = tc.blockNumber()

        should_comment = l1 + 1 - l0
        for i in range(l0, l1+1):
            b = self.document().findBlockByNumber(i)
            s = b.text().lstrip()
            if len(s)>0:
                if s[0] == '%':
                    should_comment -= 1

        for i in range(l0, l1+1):
            b = self.document().findBlockByNumber(i)
            tstrip = b.text().lstrip()
            tc.setPosition(b.position())
            tc.movePosition(QTextCursor.Right, n=len(b.text()) - len(tstrip))
            if should_comment:
                tc.insertText('% ')
            else:
                n=0
                n += 1 if tstrip[0]=='%' else 0
                n += 1 if tstrip[1]==' ' else 0
                for _ in range(n):
                    tc.deleteChar()

    def find(self, word, back):
        # word = 'prova'
        tc = self.textCursor()
        if back:
            tc = self.document().find(word, tc.anchor(), QTextDocument.FindBackward)
        else:
            tc = self.document().find(word, tc.position())
        print(tc.position())
        if tc.position() == -1:
            return
        self.setTextCursor(tc)

        
class FileEditor(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setStyleSheet(style.editor_style)
        self.setPalette(settings.editor["palette"])
        self.setFont(settings.editor["font"])
        self.setAutoFillBackground(True)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_file)
        self.currentChanged.connect(self.onTabChanged)
        self.files = []

        def wrapper(f):
            def inner():
                w = self.currentWidget()
                if not w is None:
                    getattr(w, f)()
            return inner
        
        for f in ['undo','redo','cut','copy','paste','comment']:
            setattr(self, f, wrapper(f))


    def text_changed(self, changed):
        e = self.sender()
        idx = self.files.index(e.filename)
        if changed:
            self.setTabText(idx, f'* {self.tabText(idx)[2:-1]} ')

    def save_file(self):
        idx = self.currentIndex()
        e: Editor = self.currentWidget()
        with open(e.filename, 'w') as f:
            f.write(e.document().toPlainText())
        self.setTabText(idx, f'  {self.tabText(idx)[2:-1]} ')
        e.document().setModified(False)

    def load_file(self, filename):
        if not filename in self.files:
            e = Editor(self, filename)  
            e.modificationChanged.connect(self.text_changed)
            self.addTab(e, f'  {os.path.basename(filename)} ')
            self.files.append(filename)
        idx = self.files.index(filename)
        self.setCurrentIndex(idx)

    def onTabChanged(self, idx):
        completer.closeAll()
        if idx > -1:
            completer.setEditor(self.widget(idx))

    def close_file(self, idx):
        self.removeTab(idx)
        self.files.remove(self.files[idx])

    def file_obsolete(self, filename):
        if filename in self.files:
            idx = self.files.index(filename)
            self.close_file(idx)

    def find(self, word, back):
        print(word)
        w = self.currentWidget()
        if not w is None:
            w.find(word, back)

    # def onFileChanged(self, path):
    #     idx = self.files.index(path)
    #     if not os.path.exists(path):
    #         self.close_file(idx)
    #     else: # changed content, not file name
    #         if not self.has_saved:
    #             # destroy editor and create new one
    #             self.close_file(idx)
    #             self.load_file(path)
    #             end = self.tabBar().count()
    #             self.tabBar().move(end - 1, idx)
    #     self.has_saved = False