from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtGui import QIconEngine, QIcon, QImage, QPixmap, QPainter, qRgba
from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import QRectF, Qt, QRect, QPoint

def setAttrRecur(elem, tag, attr, val):
    if elem.tagName()==tag:
        elem.setAttribute(attr, val)
    else:
        for i in range(elem.childNodes().count()):
            if (not elem.childNodes().at(i).isElement()):
                continue
            else:
                setAttrRecur(elem.childNodes().at(i).toElement(), tag, attr, val)

class SVGIconEngine(QIconEngine):
    def __init__(self, s):
        self.svg = s
        super().__init__()

    def paint(self, painter, rect, mode, state):
        r = QSvgRenderer(self.svg)
        r.render(painter, QRectF(rect))
        # return super().paint(painter, rect, mode, state)

    def pixmap(self, size, mode, state):
        img = QImage(size, QImage.Format_ARGB32)
        img.fill(qRgba(0, 0, 0, 0))
        pix = QPixmap.fromImage(img, Qt.NoFormatConversion)

        painter = QPainter(pix)
        r = QRect(QPoint(0, 0), size)
        self.paint(painter, r, mode, state)

        return pix
        # return super().pixmap(size, mode, state)

class SVG:
    def __init__(self, svg):
        self.svg = svg.encode('utf-8') if type(svg) is str else svg
        self.doc = QDomDocument()
        self.doc.setContent(self.svg)

    def setAttr(self, tag, attr, val):
        setAttrRecur(self.doc.documentElement(), tag, attr, val)

    def getQSvgWidget(self):
        svg = QSvgWidget()
        svg.load(bytearray(self.doc.toByteArray()))
        return svg
    
    def getQIcon(self):
        return QIcon(SVGIconEngine(self.doc.toByteArray()))

def create_icons(s, *args):
    out = []
    for a in args:
        svg = SVG(s)
        svg.setAttr("svg", "stroke", a)
        svg.setAttr("path", "stroke", a)
        svg.setAttr("polyline", "stroke", a)
        # svg.setAttr("path", "fill", a)
        out += [svg.getQIcon()]
    return out
  