from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QIconEngine, QIcon, QImage, QPixmap, QPainter, qRgba
from PyQt6.QtCore import QRectF, Qt, QRect, QPoint
from PyQt6.QtXml import QDomDocument

import xml.etree.ElementTree as ET

class SVGIconEngine(QIconEngine):
    def __init__(self, s):
        self.svg = s
        super().__init__()

    def paint(self, painter, rect, mode, state):
        r = QSvgRenderer(self.svg)
        r.render(painter, QRectF(rect))

    def pixmap(self, size, mode, state):        
        img = QImage(size, QImage.Format.Format_ARGB32)
        img.fill(qRgba(0, 0, 0, 0))
        pix = QPixmap.fromImage(img, Qt.ImageConversionFlag.NoFormatConversion)

        painter = QPainter(pix)
        r = QRect(QPoint(0, 0), size)
        self.paint(painter, r, mode, state)

        return pix


# def setAttr(root, tag, attr, val):
#     if root.tag.split('}')[1] == tag:
#         root.attrib[attr] = val
#     else:
#         for child in root:
#             setAttr(child, tag, attr, val)
def setAttrRecur(elem, tag, attr, val):
    if elem.tagName()==tag:
        elem.setAttribute(attr, val)
    else:
        for i in range(elem.childNodes().count()):
            if (not elem.childNodes().at(i).isElement()):
                continue
            else:
                setAttrRecur(elem.childNodes().at(i).toElement(), tag, attr, val)



class SVG:
    def __init__(self, svg: str):
        # self.svg = svg
        self.svg = svg.encode('utf-8') if type(svg) is str else svg
        self.doc = QDomDocument()
        self.doc.setContent(self.svg)
        # self.root = ET.fromstring(svg)

    def setAttr(self, tag, attr, val):
        # setAttrRecur(self.root, tag, attr, val)
        setAttrRecur(self.doc.documentElement(), tag, attr, val)

    # def data(self):
    #     return ET.tostring(self.root)
    
    def getQIcon(self):
        return QIcon(SVGIconEngine(self.doc.toByteArray()))
        # return QIcon(SVGIconEngine(ET.tostring(self.root)))


def create_icon(s, *args):
    svg = SVG(s)
    for (a, v) in args:
        svg.setAttr("svg", a, v)
        svg.setAttr("path", a, v)
        svg.setAttr("polyline", a, v)
        # svg.setAttr("path", "fill", a)
        # out += [svg.getQIcon()]
    return svg.getQIcon()
  