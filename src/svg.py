from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtGui import QIconEngine, QIcon, QImage, QPixmap, QPainter, qRgba
from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import QRectF, Qt, QRect, QPoint, QSize

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
        # re = QRectF(0, 0, rect.width()*2, rect.height() * 2)
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



class SVG:
    def __init__(self, svg):
        self.svg = svg.encode('utf-8') if type(svg) is str else svg
        # self.bytearray = bytearray(self.svg)
        self.doc = QDomDocument()
        self.doc.setContent(self.svg)

    def setAttr(self, tag, attr, val):
        setAttrRecur(self.doc.documentElement(), tag, attr, val)

    def getQSvgWidget(self, scale = 1):
        svg = QSvgWidget()
        # svg.load(self.bytearray)
        svg.load(bytearray(self.doc.toByteArray()))
        size = svg.sizeHint()
        svg.setFixedHeight(int(size.height() * scale))
        svg.setFixedWidth(int(size.width() * scale))
        return svg
    
    def getQIcon(self):
        # return QIcon(SVGIconEngine(self.bytearray))
        return QIcon(SVGIconEngine(self.doc.toByteArray()))


def create_icon(s, *args):
    svg = SVG(s)
    for (a, v) in args:
        svg.setAttr("svg", a, v)
        svg.setAttr("path", a, v)
        svg.setAttr("polyline", a, v)
        # svg.setAttr("path", "fill", a)
        # out += [svg.getQIcon()]
    return svg.getQIcon()
  