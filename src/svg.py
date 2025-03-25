from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QIconEngine, QIcon, QImage, QPixmap, QPainter, qRgba
from PyQt5.QtCore import QRectF, Qt, QRect, QPoint, QSize

class SVGIconEngine(QIconEngine):
    def __init__(self, s):
        self.svg = s
        super().__init__()

    def paint(self, painter, rect, mode, state):
        r = QSvgRenderer(self.svg)
        r.render(painter, QRectF(rect))

    def pixmap(self, size, mode, state):        
        img = QImage(size, QImage.Format_ARGB32)
        img.fill(qRgba(0, 0, 0, 0))
        pix = QPixmap.fromImage(img, Qt.NoFormatConversion)

        painter = QPainter(pix)
        r = QRect(QPoint(0, 0), size)
        self.paint(painter, r, mode, state)

        return pix


def setAttr(root, tag, attr, val):
    if root.tag.split('}')[1] == tag:
        root.attrib[attr] = val
    else:
        for child in root:
            setAttr(child, tag, attr, val)

import xml.etree.ElementTree as ET

class SVG:
    def __init__(self, svg: str):
        self.svg = svg
        self.root = ET.fromstring(svg)

    def setAttr(self, tag, attr, val):
        setAttr(self.root, tag, attr, val)
    
    def data(self):
        return ET.tostring(self.root)
    
    def getQIcon(self):
        return QIcon(SVGIconEngine(ET.tostring(self.root)))


def create_icon(s, *args):
    svg = SVG(s)
    for (a, v) in args:
        svg.setAttr("svg", a, v)
        svg.setAttr("path", a, v)
        svg.setAttr("polyline", a, v)
        # svg.setAttr("path", "fill", a)
        # out += [svg.getQIcon()]
    return svg.getQIcon()
  