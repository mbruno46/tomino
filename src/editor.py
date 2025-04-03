import os

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QTabWidget, QWidget, QPlainTextEdit
from PyQt6.QtGui import QPainter, QColor, QFontMetricsF, QKeyEvent, QTextCursor, QTextDocument

from highligher import Highlighter
import settings
import style
from autocompleter import AutoCompleter


completer = AutoCompleter()

class Editor(QPlainTextEdit):

    class NumberBar(QWidget):
        def __init__(self, editor):
            super().__init__(editor)
            self.editor = editor

            width = self.fontMetrics().averageCharWidth()*5 + 10
            self.setFixedWidth(width)
            self.editor.setViewportMargins(width, 0, 0, 0)

            self.editor.updateRequest.connect(self.updateContents) 
            self.editor.blockCountChanged.connect(lambda x: print('bcc ', x))

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
                painter.drawText(paint_rect, Qt.AlignmentFlag.AlignRight, str(blockNumber+1))
 
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
        if event.key() == Qt.Key.Key_Tab:
            self.indent(False)
            return
        if event.key() == Qt.Key.Key_Backtab:
            self.indent(True)
            return
        
        super().keyPressEvent(event)
        completer.check_and_launch()

        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.indent_newline()
        


    def selected_lines(self):
        tc = self.textCursor()

        if tc.hasSelection():
            start, end = tc.selectionStart(), tc.selectionEnd()
            tc.setPosition(start)
            l0 = tc.blockNumber()
            tc.setPosition(end)
            l1 = tc.blockNumber()
        else:
            l0 = l1 = tc.blockNumber()
        return tc, l0, l1
    
    def indent_newline(self): 
        tc, l0, l1 = self.selected_lines()
        b = self.document().findBlockByNumber(l0-1)
        n = len(b.text()) - len(b.text().lstrip())
        tc.insertText(' ' * n)

    def indent(self, shift):
        tc, l0, l1 = self.selected_lines()
        for i in range(l0, l1+1):
            b = self.document().findBlockByNumber(i)
            tc.setPosition(b.position())
            if shift:
                tstrip = b.text().lstrip()
                n = min(len(b.text()) - len(tstrip), settings.editor["tab"])
                tc.movePosition(QTextCursor.MoveOperation.Right, tc.MoveMode.KeepAnchor, n)
                tc.deleteChar()
            else:
                tc.insertText(' ' * settings.editor["tab"])
            
    def comment(self):
        tc, l0, l1 = self.selected_lines()

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
        tc = self.textCursor()
        if back:
            tc = self.document().find(word, tc.anchor(), QTextDocument.FindFlag.FindBackward)
        else:
            tc = self.document().find(word, tc.position())
        if tc.position() == -1:
            return
        self.setTextCursor(tc)
        self.setFocus()

    def focus_on_line(self, number):
        tc = self.textCursor()
        b = self.document().findBlockByNumber(number)
        tc.setPosition(b.position())
        self.setTextCursor(tc)

class FileEditor(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setStyleSheet(style.editor_style)
        self.setPalette(settings.editor["palette"])
        self.setFont(settings.editor["font"])
        self.setAutoFillBackground(True)
        self.setUsesScrollButtons(True)
        self.setElideMode(Qt.TextElideMode.ElideNone)

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

        def wrapper_setCurrentIndex(i):
            def inner():
                self.setCurrentIndex(i)
            return inner
        
        for i in range(4):
            setattr(self, f'setCurrentIndex{i+1}', wrapper_setCurrentIndex(i))

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

    def close_all(self):
        for i in reversed(range(len(self.files))):
            self.close_file(i)

    def file_obsolete(self, filename):
        if filename in self.files:
            idx = self.files.index(filename)
            self.close_file(idx)

    def find(self, word, back):
        w = self.currentWidget()
        if not w is None:
            w.find(word, back)

    def focus_on_line(self, filename, idx):
        self.load_file(filename)
        e: Editor = self.currentWidget()
        e.focus_on_line(idx)
        e.setFocus()

