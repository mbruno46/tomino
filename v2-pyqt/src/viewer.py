from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QToolBar, QAction
# from PyQt5.QtWeb import QWebEngineView , QWebEngineSettings
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QIcon
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5.QtCore import QByteArray, QSize, Qt
from PyQt5.QtXml import QDomDocument
import pymupdf

import settings
import style
import svg

svg_icons = {
    "Zoom In": '<svg viewBox="0 -0.5 21 21" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>zoom_in [#1462]</title> <desc>Created with Sketch.</desc> <defs> </defs> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="Dribbble-Light-Preview" transform="translate(-379.000000, -440.000000)" fill="#000000"> <g id="icons" transform="translate(56.000000, 160.000000)"> <path d="M332.449994,286.967331 L334.549993,286.967331 C335.129593,286.967331 335.599993,287.416448 335.599993,287.969825 C335.599993,288.523201 335.129593,288.972319 334.549993,288.972319 L332.449994,288.972319 L332.449994,290.977306 C332.449994,291.530683 331.979595,291.9798 331.399995,291.9798 C330.820395,291.9798 330.349996,291.530683 330.349996,290.977306 L330.349996,288.972319 L328.249997,288.972319 C327.670397,288.972319 327.199998,288.523201 327.199998,287.969825 C327.199998,287.416448 327.670397,286.967331 328.249997,286.967331 L330.349996,286.967331 L330.349996,284.962344 C330.349996,284.408967 330.820395,283.95985 331.399995,283.95985 C331.979595,283.95985 332.449994,284.408967 332.449994,284.962344 L332.449994,286.967331 Z M343.692338,299.706019 L343.692338,299.706019 C343.282838,300.097994 342.617138,300.097994 342.207639,299.706019 L338.060141,295.746169 L339.54484,294.328642 L343.692338,298.288493 C344.102887,298.679465 344.102887,299.315046 343.692338,299.706019 L343.692338,299.706019 Z M331.399995,294.034912 C327.926597,294.034912 325.099999,291.337201 325.099999,288.01995 C325.099999,284.7037 327.926597,282.004987 331.399995,282.004987 C334.873393,282.004987 337.699991,284.7037 337.699991,288.01995 C337.699991,291.337201 334.873393,294.034912 331.399995,294.034912 L331.399995,294.034912 Z M331.399995,280 C326.761098,280 323,283.590932 323,288.01995 C323,292.449969 326.761098,296.039899 331.399995,296.039899 C336.038892,296.039899 339.79999,292.449969 339.79999,288.01995 C339.79999,283.590932 336.038892,280 331.399995,280 L331.399995,280 Z" id="zoom_in-[#1462]"> </path> </g> </g> </g> </g></svg>',
    "Zoom out": '<svg viewBox="0 -0.5 21 21" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title>zoom_out [#1460]</title> <desc>Created with Sketch.</desc> <defs> </defs> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="Dribbble-Light-Preview" transform="translate(-59.000000, -480.000000)" fill="#000000"> <g id="icons" transform="translate(56.000000, 160.000000)"> <path d="M8.37269901,326.967331 L14.8199378,326.967331 C15.4130838,326.967331 15.8944776,327.416448 15.8944776,327.969825 C15.8944776,328.523201 15.4130838,328.972319 14.8199378,328.972319 L8.37269901,328.972319 C7.77955304,328.972319 7.29815921,328.523201 7.29815921,327.969825 C7.29815921,327.416448 7.77955304,326.967331 8.37269901,326.967331 L8.37269901,326.967331 Z M23.6848912,338.288493 C24.1050363,338.679465 24.1050363,339.315046 23.6848912,339.706019 L23.6848912,339.706019 C23.2647461,340.097994 22.5845624,340.097994 22.1654919,339.706019 L17.7888913,335.746169 L19.3082906,334.328642 L23.6848912,338.288493 Z M11.5963184,334.034912 C8.04174075,334.034912 5.14907961,331.337201 5.14907961,328.01995 C5.14907961,324.7037 8.04174075,322.004987 11.5963184,322.004987 C15.1508961,322.004987 18.0435572,324.7037 18.0435572,328.01995 C18.0435572,331.337201 15.1508961,334.034912 11.5963184,334.034912 L11.5963184,334.034912 Z M11.5963184,320 C6.84900157,320 3,323.590932 3,328.01995 C3,332.449969 6.84900157,336.039899 11.5963184,336.039899 C16.3436353,336.039899 20.1926368,332.449969 20.1926368,328.01995 C20.1926368,323.590932 16.3436353,320 11.5963184,320 L11.5963184,320 Z" id="zoom_out-[#1460]"> </path> </g> </g> </g> </g></svg>',
    "Fit Width": '<svg fill="#000000" viewBox="0 0 24 24" id="left-right-scroll-bar" data-name="Flat Line" xmlns="http://www.w3.org/2000/svg" class="icon flat-line"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><polyline id="primary" points="15 10 17 12 15 14" style="fill: none; stroke: #000000; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><polyline id="primary-2" data-name="primary" points="9 14 7 12 9 10" style="fill: none; stroke: #000000; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><path id="primary-3" data-name="primary" d="M21,6V18M3,6V18m14-6H7" style="fill: none; stroke: #000000; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></path></g></svg>',
    "Fit Height": '<svg fill="#000000" viewBox="0 0 24 24" id="up-down-scroll-bar" data-name="Flat Line" xmlns="http://www.w3.org/2000/svg" class="icon flat-line"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><polyline id="primary" points="10 9 12 7 14 9" style="fill: none; stroke: #000000; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><polyline id="primary-2" data-name="primary" points="14 15 12 17 10 15" style="fill: none; stroke: #000000; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><path id="primary-3" data-name="primary" d="M6,3H18M6,21H18M12,7V17" style="fill: none; stroke: #000000; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></path></g></svg>',
    "Invert colors": '<svg fill="#000000" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" d="M4,14 C4,11.0544813 6.66666667,7.05448133 12,2 C17.3333333,7.05448133 20,11.0544813 20,14 C20,18.3349143 16.5521622,21.8645429 12.2491793,21.9961932 L12,22 C7.581722,22 4,18.418278 4,14 Z M12,4.793 L11.7832437,5.01193635 C7.89798368,8.95774552 6,12.0287291 6,14 C6,17.3137085 8.6862915,20 12,20 L12,4.793 Z"></path> </g></svg>',
}


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
    class ToolBar(QToolBar):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.setOrientation(Qt.Horizontal)
            self.setIconSize(QSize(48, 48))
            self.setPalette(settings.app["palette"])

            theme = settings.get_theme()

            self.icons = []
            self.actions = []
            for key in svg_icons:
                self.icons += [svg.create_icons(svg_icons[key], theme['gray'], theme['text'])]
                btn = QAction(key, self)
                btn.setIcon(self.icons[-1][0])

                self.actions.append(btn)
                self.addAction(btn)

            self.actionTriggered.connect(self.trigger)
            self.active = 0


        def trigger(self, action):
            self.actions[self.active].setIcon(self.icons[self.active][0])

            idx = self.actions.index(action)
            # self.parent.browser.setCurrentIndex(idx)
            self.active = idx

            action.setIcon(self.icons[idx][1])            

    def __init__(self, app):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet(style.viewer_style)

        toolbar = self.ToolBar(self) #QWidget()
        # toolbar.setLayout(QHBoxLayout())
        self.layout().addWidget(toolbar)

        self.scroll = QScrollArea(widgetResizable=True)
        self.pdfviewer = PDFViewer(self)
        self.pdfviewer.setPalette(settings.viewer["palette"])
        self.scroll.setWidget(self.pdfviewer)
        self.layout().addWidget(self.scroll)
        self.invertPixels = False

        # # fill toolbar after creation of pdfviewer
        # for icon, func in [
        #     ('+', self.pdfviewer.zoomin),
        #     ('-', self.pdfviewer.zoomout),
        #     ('W', self.pdfviewer.fitW),
        #     ('H', self.pdfviewer.fitH),
        #     ('I', self.pdfviewer.swapTheme)
        # ]:
        #     btn = QPushButton(self)
        #     btn.setText(icon)
        #     btn.clicked.connect(func)
        #     toolbar.layout().addWidget(btn)

    def load(self, path = None):
        self.pdfviewer.load(path)



