from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextCursor

# class Keywords:
#     def __init__(self, keywords, shift_backward):
#         self.keywords = keywords
#         self.shift_backward = shift_backward

#     def __call__(self):
#         return self.keywords
    
#     def complete(self, editor, choice):
#         tc = editor.textCursor()
#         word = editor.trigger_word
#         tc.insertText(choice[len(word):])
#         if self.shift_backward > 0:
#             tc.movePosition(QTextCursor.Left, n=self.shift_backward)
#         editor.setTextCursor(tc)

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

class Base(QCompleter):
    def __init__(self, editor):
        self.keywords = math + cmds
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



class AutoCompleter:
    def __init__(self, editor):
        self.basic = AutoCompleterBasic(editor)
        self.editor = editor
        self.min_left = self.editor.number_bar.width()

    def isVisible(self):
        v = self.basic.popup().isVisible()
        return v
    
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
        word = self.trigger_word
        if not word:
            return
        
        if word[0]=='\\':
            _completer = self.basic
        else:
            return

        print(word, word[0]=='\\', _completer)

        _completer.setCompletionPrefix(word)
        popup = _completer.popup()

        cr = self.editor.cursorRect()
        popup.setCurrentIndex(_completer.completionModel().index(0, 0))
        cr.setWidth(
            _completer.popup().sizeHintForColumn(0)
            + _completer.popup().verticalScrollBar().sizeHint().width()
            + self.min_left
        )
        cr.setX(cr.x() + self.min_left)
        _completer.complete(cr)


