from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt, QRegExp, QRegularExpression
from PyQt5.QtGui import QTextCursor, QFontMetrics

import json, os
for _f in ['math', 'cmds', 'envs']:
    with open(f'{os.path.dirname(__file__)}/latex.{_f}.json','r') as f:
        globals()[_f] = json.load(f)


class Base(QCompleter):
    def __init__(self, keywords):
        self.keywords = keywords
        super().__init__(self.keywords)

        self.setModelSorting(QCompleter.CaseSensitivelySortedModel)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setWrapAround(False)
        self.activated.connect(self.onActivated)

    def setEditor(self, editor):
        self.setWidget(editor)
        self.popup().setFont(editor.font())
        self.popup().setPalette(editor.palette())

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

    def delete_left_nchars(self, n):
        tc = self.widget().textCursor()
        tc.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, n=n)
        tc.deletePreviousChar()

    def onActivated(self, choice, func):
        new_text, shift_backward = func(choice)

        editor = self.widget()
        tc = editor.textCursor()
        tc.insertText(new_text)
        tc.movePosition(QTextCursor.Left, n=shift_backward)        
        editor.setTextCursor(tc)

    def update_keyword(self, value, remove):
        m = self.model()
        if remove:
            print(m.stringList())
            idx = m.stringList().index(value)
            m.removeRow(idx)
            print(value, idx, m.stringList())
        else:
            if m.insertRow(m.rowCount()):
                idx = m.index(m.rowCount() - 1, 0)
                m.setData(idx, value)

    def clean(self):
        m = self.model()
        m.removeRows(0, m.rowCount())

    def __call__(self):
        pass

class AutoCompleterBasic(Base):
    def onActivated(self, choice):
        def inner(choice):
            word = self.completionPrefix()
            shift_backward = 0
            re = QRegExp(r"\\[a-zA-Z]+\[\]\{\}")
            if re.indexIn(choice) == 0:
                shift_backward = 3
            re = QRegExp(r"\\[a-zA-Z]+\{\}")
            if re.indexIn(choice) == 0:
                shift_backward = 1
            return choice[len(word):], shift_backward

        super().onActivated(choice, inner)

class AutoCompleterEnvironments(Base):
    def onActivated(self, choice):
        def inner(choice):
            self.delete_right_matching_char('}')
            word = self.completionPrefix()
            t = choice[len(word):] + "}" + "\n" + f"\n\\end{{{choice}}}"
            return t, 7 + len(choice)

        super().onActivated(choice, inner)

class AutoCompleterGeneric(Base):
    def onActivated(self, choice):
        def inner(choice):
            self.delete_right_matching_char('}')
            word = self.completionPrefix()
            t = choice[len(word):] + "}"
            return t, 0

        super().onActivated(choice, inner)

class AutoCompleterMultiple(Base):
    def __init__(self):
        self.kwrds = {}
        self.changed = True
        super().__init__([])

    def __call__(self):
        if self.changed:
            all_keywords = []
            for key in self.kwrds:
                all_keywords += self.kwrds[key]
            self.model().setStringList(all_keywords)
            self.changed = False

    def append(self, tag, words):
        if not tag in self.kwrds:
            self.kwrds[tag] = []
        self.kwrds[tag].append(words)
        self.changed = True

    def extend(self, tag, words):
        if not tag in self.kwrds:
            self.kwrds[tag] = []
        self.kwrds[tag].extend(words)
        self.changed = True

    def remove(self, tag, word):
        if not tag in self.kwrds:
            return
        self.kwrds[tag].remove(word)
        self.changed = True

    def delete(self, tag):
        if tag in self.kwrds:
            del self.kwrds[tag]
        self.changed = True

    def clean(self):
        self.kwrds = {}
        self.changed = True
        self()

class AutoCompleterRef(AutoCompleterMultiple):
    def onActivated(self, choice):
        def inner(choice):
            self.delete_right_matching_char('}')
            word = self.completionPrefix()
            t = choice[len(word):] + "}"
            return t, 0

        super().onActivated(choice, inner)

class AutoCompleterCite(AutoCompleterMultiple):
    def __init__(self):
        super().__init__()
        self.setFilterMode(Qt.MatchContains)

    def onActivated(self, choice):
        def inner(choice):
            self.delete_right_matching_char('}')
            word = self.completionPrefix()
            self.delete_left_nchars(len(word))
            choice = choice.split(' [')[0]
            t = choice + "}"
            return t, 0

        super().onActivated(choice, inner)

input = AutoCompleterGeneric([])
bibliography = AutoCompleterGeneric([])
includegraphics = AutoCompleterGeneric([])
ref = AutoCompleterRef()
cite = AutoCompleterCite()

class AutoCompleter:
    def __init__(self):
        self.basic_completer = AutoCompleterBasic(math + cmds)
        self.completers = {
            'begin': AutoCompleterEnvironments(envs),
            'input': input,
            'bibliography': bibliography,
            'includegraphics': includegraphics,
            'ref': ref,
            'cite': cite,
        }
        # in case basic_completer has inserted text, e.g. \begin{}
        # then a new completer should be fired
        self.basic_completer.activated.connect(self.check_and_launch)

    def isVisible(self):
        if self.basic_completer.isVisible():
            return True
        for c in self.completers.values():
            if c.isVisible():
                return True
    
    def closeAll(self):
        self.basic_completer.close()
        for c in self.completers.values():
            c.close()

    @property
    def trigger_word(self):
        tc = self.editor.textCursor()
        while True:
            if tc.atStart() or tc.atBlockStart() or tc.hasSelection():
                break
            else:
                tc.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
                if tc.selectedText()[0] == "\\":
                    break
        return tc.selectedText()
    
    def check_and_launch(self):
        self.closeAll()
        _completer: QCompleter = None

        word = self.trigger_word
        if not word:
            return

        if word[0]=='\\':
            for trigger in self.completers:
                re = QRegularExpression(r'\\%s(\[.*?\])?\{' % trigger)
                m = re.globalMatch(word)
                if m.hasNext():
                    n = len(m.next().captured(0))
                    _completer = self.completers[trigger]
                    word = word[n:]
                    print('activate ', input, _completer.model().stringList())
                    break

            _completer = self.basic_completer if _completer is None else _completer
        else:
            return

        _completer() # performs internal updates if needed
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


    def setEditor(self, editor):
        self.basic_completer.setEditor(editor)
        for key in self.completers:
            self.completers[key].setEditor(editor)
        self.editor = editor
        self.min_left = self.editor.number_bar.width()

    def reset(self):
        self.completers['input'].clean()
        self.completers['bibliography'].clean()
        self.completers['includegraphics'].clean()
        self.completers['ref'].clean()
        self.completers['cite'].clean()

       
