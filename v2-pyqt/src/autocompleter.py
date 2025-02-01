from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt, QRegExp, QStringListModel
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
input = []

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

    def delete_right_matching_char(self, char):
        tc = self.widget().textCursor()
        if (not tc.atEnd()) or (not tc.atBlockEnd()):
            tc.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            if tc.selectedText()[0]==char:
                tc.deletePreviousChar()

    def onActivated(self, choice, func):
        new_text, shift_backward = func(choice)

        editor = self.widget()
        tc = editor.textCursor()
        tc.insertText(new_text)
        tc.movePosition(QTextCursor.Left, n=shift_backward)        
        editor.setTextCursor(tc)

    def update_keywords(self, keywords):
        m = QStringListModel(keywords)
        self.setModel(m)
        
class AutoCompleterBasic(Base):
    def onActivated(self, choice):
        def inner(choice):
            word = self.completionPrefix()
            shift_backward = 0
            re = QRegExp("\\\\[a-zA-Z]+\\{\\}")
            if re.indexIn(choice) == 0:
                shift_backward = 3
            re = QRegExp("\\\\[a-zA-Z]+\\{\\}")
            if re.indexIn(choice) == 0:
                shift_backward = 1
            return choice[len(word):], shift_backward

        super().onActivated(choice, inner)

class AutoCompleterEnvironments(Base):
    def onActivated(self, choice):
        # editor = self.widget()
        # tc = editor.textCursor()
        # if (not tc.atEnd()) or (not tc.atBlockEnd()):
        #     tc.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        #     if tc.selectedText()[0]=='}':
        #         tc.deletePreviousChar()
        def inner(choice):
            self.delete_right_matching_char('}')
            word = self.completionPrefix()
            t = choice[len(word):] + "}" + "\n" + f"\n\\end{{{choice}}}"
            return t, 7 + len(choice)

        super().onActivated(choice, inner)

class AutoCompleterInput(Base):
    def onActivated(self, choice):
        def inner(choice):
            self.delete_right_matching_char('}')
            word = self.completionPrefix()
            t = choice[len(word):] + "}"
            return t, 0

        super().onActivated(choice, inner)


class AutoCompleter:
    def __init__(self, editor):
        self.completers = [
            AutoCompleterBasic(math + cmds, editor),
            AutoCompleterEnvironments(envs, editor),
            AutoCompleterInput(input, editor),
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
            if word[0:7]=='\\begin{':
                _completer = self.completers[1]
                word = word[7:]
            elif word[0:7]=='\\input{':
                _completer = self.completers[2]
                word = word[7:]
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


class Parser:
    def __init__(self, main = None):
        self.main = main
        self.db = {
            'input': [],
            'bib': [],
            'label': [],
        }

    def parse(self, keyword, text):
        db = self.db[keyword]
        re = QRegExp(f'\\{keyword}\\{{(.*)\\}}')
        index = re.indexIn(text)
        # print(re.cap(1))
        re = QRegExp("\\input(\\{.*\\})")
        index = re.indexIn(text)
        print(index, re.cap(1)[0:100])
        return 
        while index >= 0:
            word = re.cap(0)
            for w in word.split(','):
                if not w in db:
                    db.append(w)
            index = re.indexIn(text, index + 9 + len(word))

    def __call__(self):
        with open(self.main,'r') as f:
            text = f.read()
            self.parse('input', text)
            self.parse('bib', text)
            self.parse('label', text)

        for f in self.db['input']:
            self.parse('label', open(self.main,'r').read())

        print(self.db)
        
parser = Parser()
refs = parser.db['label']