from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
# from PyQt5.QtWeb import QWebEngineView , QWebEngineSettings
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QIcon
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QByteArray
from PyQt5.QtXml import QDomDocument
import pymupdf

import settings
import style

class PDFViewer(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.darkTheme = False
        self.scale = 1.0
        self.page_size = None

    def load_page(self, p):

        def setAttrRecur(elem, tag, attr, val):
            if elem.tagName()==tag:
                elem.setAttribute(attr, val)
            else:
                for i in range(elem.childNodes().count()):
                    if (not elem.childNodes().at(i).isElement()):
                        continue
                    else:
                        setAttrRecur(elem.childNodes().at(i).toElement(), tag, attr, val)
 
        doc = QDomDocument()
        doc.setContent(p.get_svg_image())
        svg = QSvgWidget()

        if self.darkTheme:
            setAttrRecur(doc.documentElement(), "path", "fill", settings.get_theme()['text'])
        else:
            svg.setStyleSheet('QSvgWidget {background:  white}')

        svg.load(bytearray(doc.toByteArray()))
        size = svg.sizeHint()
        svg.setFixedHeight(int(size.height() * self.scale))
        svg.setFixedWidth(int(size.width() * self.scale))
        self.page_size = size
        return svg

    
    def load(self, path = None):
        # self.path = "/Users/mbruno/Physics/talks/valencia_19/valencia_19.pdf"
        self.path = "/Users/mbruno/Physics/notes/sf-dwf/sf-dwf.pdf"
        # self.path = "/Users/mbruno/Physics/ToM/dummy/main3.pdf"
        doc = pymupdf.open(self.path)

        for i in reversed(range(self.layout().count())): 
            self.layout().itemAt(i).widget().setParent(None)
    
        for i, p in enumerate(doc):
            page = self.load_page(p)
            self.layout().addWidget(page)
        
        doc.close()

    def swapTheme(self):
        self.darkTheme = not self.darkTheme
        self.load()

    def zoomin(self):
        if self.scale<2.0:
            self.scale += 0.1
            self.load()

    def zoomout(self):
        if self.scale>0.2:
            self.scale -= 0.1
            self.load()

    def fitW(self):
        if self.page_size:
            self.scale = self.parent().width() / self.page_size.width()
            self.load()

    def fitH(self):
        if self.page_size:
            self.scale = self.parent().height() / self.page_size.height()
            self.load()


class Viewer(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet(style.viewer_style)

        toolbar = QWidget()
        toolbar.setLayout(QHBoxLayout())
        self.layout().addWidget(toolbar)

        self.scroll = QScrollArea(widgetResizable=True)
        self.pdfviewer = PDFViewer(self)
        self.pdfviewer.setPalette(settings.viewer["palette"])
        self.scroll.setWidget(self.pdfviewer)
        self.layout().addWidget(self.scroll)
        self.invertPixels = False

        # fill toolbar after creation of pdfviewer
        for icon, func in [
            ('+', self.pdfviewer.zoomin),
            ('-', self.pdfviewer.zoomout),
            ('W', self.pdfviewer.fitW),
            ('H', self.pdfviewer.fitH),
            ('I', self.pdfviewer.swapTheme)
        ]:
            btn = QPushButton(self)
            btn.setText(icon)
            btn.clicked.connect(func)
            toolbar.layout().addWidget(btn)

    def load(self, path = None):
        self.pdfviewer.load(path)



