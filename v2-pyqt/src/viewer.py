from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
# from PyQt5.QtWeb import QWebEngineView , QWebEngineSettings
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QIcon
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QByteArray
from PyQt5.QtXml import QDomDocument
import pymupdf

import settings

class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.darkTheme = False
        
    def removeLastPages(self, n):
        N = len(self.layout().children())
        for i in range(n):
            w = self.layout().takeAt(N-1-i)
            w.widget().setParent(None)
            # self.layout().removeItem(w)

    def load_page(self, p):
        # pix = p.get_pixmap(dpi=240)
        # print(pix.xres, pix.yres)
        # # pix.set_dpi(pix.xres* 10, pix.yres*10)
        # # print(pix.xres, pix.yres)
        # fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        # qimage = QImage(pix.samples_ptr, pix.width, pix.height, fmt)
        # if self.invertPixels:
        #     qimage.invertPixels()
        # page = QLabel()
        # page.setFixedHeight(pix.height)
        # page.setPixmap(QPixmap.fromImage(qimage))
        # return page

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
        svg.setFixedHeight(size.height())
        svg.setFixedWidth(size.width())
        return svg

    
    def load(self, path = None):
        self.path = "/Users/mbruno/Physics/talks/valencia_19/valencia_19.pdf"
        # self.path = "/Users/mbruno/Physics/notes/sf-dwf/sf-dwf.pdf"
        # self.path = "/Users/mbruno/Physics/ToM/dummy/main3.pdf"
        doc = pymupdf.open(self.path)
        # doc.load_page(0).get_svg_image
        for i in reversed(range(self.layout().count())): 
            self.layout().itemAt(i).widget().setParent(None)
    
        for i, p in enumerate(doc):
            # page = QLabel()
            # qimage = self.load_page(p)
            # page.setPixmap(QPixmap.fromImage(qimage))
            # self.layout().addWidget(page)

            # pix = p.get_pixmap(dpi=100)
            # fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
            # print(fmt, QImage.Format_RGB888)
            # qimage = QImage(pix.samples_ptr, pix.width, pix.height, QImage.Format_RGB888)
            # page = QLabel('page')
            # # page.setFixedHeight(pix.height)
            # page.setPixmap(QPixmap.fromImage(qimage.rgbSwapped()))
            # print(page.width())

            page = self.load_page(p)
            # print(page.width())/
            self.layout().addWidget(page)
        
        doc.close()

    def swapTheme(self):
        self.darkTheme = not self.darkTheme
        self.load()


class Viewer(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setLayout(QVBoxLayout())

        toolbar = QWidget()
        toolbar.setLayout(QHBoxLayout())
        self.layout().addWidget(toolbar)

        self.scroll = QScrollArea(widgetResizable=True)
        self.pdfviewer = PDFViewer()
        self.scroll.setWidget(self.pdfviewer)
        self.layout().addWidget(self.scroll)
        self.invertPixels = False

        # fill toolbar after creation of pdfviewer
        for icon, func in [
            ('+', lambda x: print('zoom')),
            ('I', self.pdfviewer.swapTheme)
        ]:
            btn = QPushButton()
            btn.setText(icon)
            btn.clicked.connect(func)
            toolbar.layout().addWidget(btn)

    def load(self, path = None):
        self.pdfviewer.load(path)



