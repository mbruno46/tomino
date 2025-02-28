from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt, QRegExp, QRegularExpression, QStringListModel
from PyQt5.QtGui import QTextCursor, QFontMetrics

import json, os
for _f in ['math', 'cmds', 'envs']:
    with open(f'./latex.{_f}.json','r') as f:
        globals()[_f] = json.load(f)

# from latex import LatexParser

# input = []
# biblio = []
# figures = []
# refs = []

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

        
class AutoCompleterBasic(Base):
    def onActivated(self, choice):
        def inner(choice):
            word = self.completionPrefix()
            shift_backward = 0
            re = QRegExp("\\\\[a-zA-Z]+\\[\\]\\{\\}")
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

class AutoCompleterGeneric(Base):
    def onActivated(self, choice):
        def inner(choice):
            self.delete_right_matching_char('}')
            word = self.completionPrefix()
            t = choice[len(word):] + "}"
            return t, 0

        super().onActivated(choice, inner)

input = AutoCompleterGeneric([])
bibliography = AutoCompleterGeneric([])
includegraphics = AutoCompleterGeneric([])
ref = AutoCompleterGeneric([])
cite = AutoCompleterGeneric([])

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
        # self.editor = editor
        # self.min_left = self.editor.number_bar.width()

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
            if tc.atStart() or tc.atBlockStart():
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
                re = QRegularExpression('\\\\%s(\\[.*?\\])?\\{' % trigger)
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


    # def update(self):
    #     print('ehre')
    #     m = self.completers['input'].model()
    #     for el in input:
    #         print(el, el in m.stringList())
    #         if not el in m.stringList():
    #             m.stringList().append(el)
    #     for el in m.stringList():
    #         if not el in input:
    #             m.stringList().remove(el)


    # def update(self, key, value, remove=False):
    #     print('ehre')
    #     m = self.completers[key].model()
    #     if remove:
    #         if value in m.stringList():
    #             m.stringList().remove(value)
    #     else:
    #         if not value in m.stringList():
    #             m.stringList().append(value)

    def setEditor(self, editor):
        self.basic_completer.setEditor(editor)
        for key in self.completers:
            self.completers[key].setEditor(editor)
        self.editor = editor
        self.min_left = self.editor.number_bar.width()

    # def file_changed(self, filename):
    #     ext = os.path.splitext(filename)[1]
    #     if ext=='.tex':


class LatexParser:
    def __init__(self, main):
        self.main = main
        self.db = {
            'input': [],
            'bibliography': [],
            'label': [],
            'cite': [],
        }
        self()

    def parse(self, keyword, text):
        db = self.db[keyword]
        # re = QRegExp(f'\\{keyword}\\{{(.*)\\}}')
        # index = re.indexIn(text)
        re = QRegExp("\\%s\{(.*)\}" % keyword)
        re.setMinimal(True)
        index = re.indexIn(text)
        while index >= 0:
            word = re.cap(1)
            for w in word.split(','):
                if not w in db:
                    db.append(w)
            index = re.indexIn(text, index + 9 + len(word))

    def parse_bib_file(self, text):
        re = QRegExp("@article\{(.*)\}")
        re.setMinimal(True)
        index = re.indexIn(text)
        while index >= 0:
            word = re.cap(1)
            print(word)

    def __call__(self, filename = None):
        if filename is None:
            with open(self.main,'r') as f:
                text = f.read()
                self.parse('input', text)
                self.parse('bibliography', text)
                self.parse('label', text)

            # for f in self.db['bibliography']:
                # self.parse_bib(open(f,'r').read())

            return
                        

        # for f in self.db['input']:
            # self.parse('label', open(f,'r').read())

        print(self.db)


# DB = LatexDB()
###
#
"""
set main creates LatexDB 

on file save, e.g. new input or new biblio --> update LatexDB refs or cites
"""


class Parser:
    def __init__(self):
        self.main = None
        self.db = {}
        
    def init(self, main):
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
        re = QRegExp("\\%s\{(.*)\}" % keyword)
        re.setMinimal(True)
        index = re.indexIn(text)
        while index >= 0:
            word = re.cap(1)
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
            self.parse('label', open(f,'r').read())

        print(self.db)
        
# parser = Parser()
# refs = parser.db['label']
