from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextCursor, QFontMetrics

math = [
    '\\frac',
    '\\dfrac'
]
cmds = [
    '\\begin{}',
    '\\end{}',
    '\\includegraphics{}',
    '\\includegraphics[]{}'
]
envs = [
    'document',
]

class Base(QCompleter):
    def __init__(self, keywords, editor):
        self.keywords = keywords
        super().__init__(self.keywords)

        self.setModelSorting(QCompleter.CaseSensitivelySortedModel)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(False)

        self.setWidget(editor)

        self.popup().setFont(editor.font())
        self.popup().setPalette(editor.palette())
        self.activated.connect(self.onActivated)

    def isVisible(self):
        return self.popup().isVisible()

    def close(self):
        self.popup().hide()

class AutoCompleterBasic(Base):
    def onActivated(self, choice):
        editor = self.widget()
        tc = editor.textCursor()
        word = self.completionPrefix()
        tc.insertText(choice[len(word):])

        shift_backward = 0
        re = QRegExp("\\\\[a-zA-Z]+\\{\\}")
        if re.indexIn(choice) == 0:
            shift_backward = 3
        re = QRegExp("\\\\[a-zA-Z]+\\{\\}")
        if re.indexIn(choice) == 0:
            shift_backward = 1
        tc.movePosition(QTextCursor.Left, n=shift_backward)
        
        editor.setTextCursor(tc)

class AutoCompleterEnvironments(Base):
    def onActivated(self, choice):
        editor = self.widget()
        tc = editor.textCursor()
        if (not tc.atEnd()) or (not tc.atBlockEnd()):
            tc.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            if tc.selectedText()[0]=='}':
                tc.deletePreviousChar()

        word = self.completionPrefix()
        tc.insertText(choice[len(word):] + "}" + "\n" + f"\n\\end{{{choice}}}")

        shift_backward = 7 + len(choice)
        tc.movePosition(QTextCursor.Left, n=shift_backward)
        
        editor.setTextCursor(tc)    

class AutoCompleter:
    def __init__(self, editor):
        self.completers = [
            AutoCompleterBasic(math + cmds, editor),
            AutoCompleterEnvironments(envs, editor)
        ]
        self.editor = editor
        self.min_left = self.editor.number_bar.width()

    def isVisible(self):
        for c in self.completers:
            if c.isVisible():
                return True
    
    def closeAll(self):
        for c in self.completers:
            c.close()

    @property
    def trigger_word(self):
        tc = self.editor.textCursor()
        while True:
            if tc.atStart() or tc.atBlockStart():
                break
            else:
                tc.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
                if tc.selectedText()[0] == "\\":
                    break
        return tc.selectedText()
    
    def check_and_launch(self):
        self.closeAll()
        _completer = None

        word = self.trigger_word
        if not word:
            return
        
        if word[0]=='\\':
            if word[0:8]=='\\begin{':
                _completer = self.completers[1]
                word = word[8:]
            else:
                _completer = self.completers[0]
        else:
            return

        _completer.setCompletionPrefix(word)
        if _completer.currentCompletion()==word:
            return

        popup = _completer.popup()

        cr = self.editor.cursorRect()
        popup.setCurrentIndex(_completer.completionModel().index(0, 0))
        delta = self.min_left - QFontMetrics(popup.font()).width(word)
        cr.setWidth(
            popup.sizeHintForColumn(0)
            + popup.verticalScrollBar().sizeHint().width()
            + delta
        )
        cr.setX(cr.x() + delta)
        #cr.y() - int(QFontMetrics(popup.font()).capHeight()))
        _completer.complete(cr)


