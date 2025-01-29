from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QTextDocument
from PyQt5 import Qt
from PyQt5.QtCore import QRegExp

import settings

def format(color):
    _color = QColor(settings.theme['dark'][color])
    fmt = QTextCharFormat()
    fmt.setForeground(_color)
    return fmt


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument) -> None:
        super().__init__(parent)
        self.formats = {}
        for tag in ['command', 'square', 'curly', 'comment']:
            self.formats[tag] = format(tag)

    # multi line support needed?
    def highlightBlock(self, text):
        re = QRegExp("(%.*)")
        index = re.indexIn(text)
        while index >= 0:
            length = len(re.cap(1))
            self.setFormat(index, length, self.formats["comment"])
            index = re.indexIn(text, index + length)

        re = QRegExp("(\\\\[a-zA-Z]+)(\\[.*\\])?(\\{.*\\})?")
        index = re.indexIn(text)
        while index >= 0:
            for i, e, c in zip([1,2,3], [0,1,1], ['command', 'square', 'curly']):
                length = len(re.cap(i))
                self.setFormat(index+e, length-2*e, self.formats[c])
                index += length
            index = re.indexIn(text, index)
