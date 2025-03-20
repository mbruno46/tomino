from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QTextDocument
from PyQt5 import Qt
from PyQt5.QtCore import QRegExp, QRegularExpression

import settings

def format(color):
    _color = QColor(color)
    fmt = QTextCharFormat()
    fmt.setForeground(_color)
    return fmt


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument) -> None:
        super().__init__(parent)
        self.formats = {}
        theme = settings.get_theme()
        for tag in ['command', 'square', 'curly', 'comment']:
            self.formats[tag] = format(theme[tag])

    def highlightBlock(self, text):
        re = QRegularExpression("(\\\\[a-zA-Z]+)(\\[.*?\\])?(\\{.*?\\})?")
        m = re.globalMatch(text)
        while m.hasNext():
            n = m.next()
            index = n.capturedStart()
            for i, e, c in zip([1,2,3], [0,1,1], ['command', 'square', 'curly']):
                length = len(n.captured(i))
                self.setFormat(index+e, length-2*e, self.formats[c])
                index += length

        re = QRegExp("(%.*)")
        index = re.indexIn(text)
        while index >= 0:
            length = len(re.cap(1))
            self.setFormat(index, length, self.formats["comment"])
            index = re.indexIn(text, index + length)

class ErrorHighligther(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument) -> None:
        super().__init__(parent)
        theme = settings.get_theme()
        self.format = format(theme['error'])
        self.force = False

    def highlightBlock(self, text):
        if QRegExp("Runaway\\sargument.*|! pdfTeX error|! LaTeX error|I found no.*").indexIn(text)>=0:
            self.force = True
        else:
            if QRegExp("l\\.\\d+").indexIn(text)>=0:
                self.setFormat(0, len(text), self.format)
                self.force = False

        if self.force:
            self.setFormat(0, len(text), self.format)
