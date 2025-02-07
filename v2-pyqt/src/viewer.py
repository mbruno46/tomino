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
    "Zoom In": '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M20 20L14.9497 14.9497M14.9497 14.9497C16.2165 13.683 17 11.933 17 10C17 6.13401 13.866 3 10 3C6.13401 3 3 6.13401 3 10C3 13.866 6.13401 17 10 17C11.933 17 13.683 16.2165 14.9497 14.9497ZM7 10H13M10 7V13" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>',
    "Zoom out": '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M20 20L14.9497 14.9498M14.9497 14.9498C16.2165 13.683 17 11.933 17 10C17 6.13401 13.866 3 10 3C6.13401 3 3 6.13401 3 10C3 13.866 6.13401 17 10 17C11.933 17 13.683 16.2165 14.9497 14.9498ZM7 10H13" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>',
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
        self.path = None

    def load_page(self, p):
        tmp = svg.SVG(p.get_svg_image())
        theme = settings.get_theme()
        if self.darkTheme:
            tmp.setAttr("path", "fill", theme['text'])
            _svg = tmp.getQSvgWidget(self.scale)
            _svg.setStyleSheet(style.set_item('QSvgWidget', f'background: {theme["text-background"]}'))
        else:
            _svg = tmp.getQSvgWidget(self.scale)
            _svg.setStyleSheet(style.set_item('QSvgWidget', f'background: white;'))

        self.page_size = _svg.sizeHint()
        return _svg

    
    def load(self):
        if self.path is None:
            return
        
        doc = pymupdf.open(self.path)

        for i in reversed(range(self.layout().count())): 
            self.layout().itemAt(i).widget().setParent(None)
    
        for i, p in enumerate(doc):
            page = self.load_page(p)
            self.layout().addWidget(page)
        
        doc.close()

    def invert(self, bool):
        self.darkTheme = bool#not self.darkTheme
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
            self.setIconSize(QSize(32, 32))
            self.setPalette(settings.app["palette"])
            # self.layout().setAlignment(Qt.AlignRight)
            # self.setAllowedAreas(Qt.RightToolBarArea)
            
        def init(self):
            theme = settings.get_theme()

            self.actions = {}
            for key, func  in zip(
                ["Zoom In", "Zoom out", "Fit Width", "Fit Height"], 
                ['zoomin', 'zoomout', 'fitW',  'fitH']):
                btn = QAction(key, self)
                btn.setCheckable(False)
                btn.triggered.connect(getattr(self.parent.pdfviewer, func))

                self.actions[func] = {
                    'action': btn, 
                    'icons': [
                        svg.create_icon(svg_icons[key],("stroke", theme['gray'])) 
                        for c in [theme['gray'], theme['text']]
                    ]
                }
                btn.setIcon(self.actions[func]['icons'][0])

            
            key = "Invert colors"
            btn = QAction(key, self)
            btn.setCheckable(True)
            btn.triggered.connect(self.invert)
            btn.trigger()

            self.actions['invert'] = {
                'action': btn, 
                'icons': [
                        svg.create_icon(svg_icons[key], 
                                        ("stroke", theme['gray']), 
                                        ("fill", theme['gray'])) 
                                        for c in [theme['gray'], theme['text']]
                    ]
            }
            btn.setIcon(self.actions['invert']['icons'][0])
            
            for key in self.actions:
                self.addAction(self.actions[key]['action'])

            # self.actionTriggered.connect(self.test)

        
        def invert(self):
            if 'invert' in self.actions:
                act = self.actions['invert']
                act['action'].setIcon(act['icons'][0 if act['action'].isChecked() else 1])
                self.parent.pdfviewer.invert(not act['action'].isChecked())

                  

    def __init__(self, app):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet(style.viewer_style)
        self.layout().setContentsMargins(4,0,0,0)
        
        toolbar = self.ToolBar(self)
        self.layout().addWidget(toolbar)

        self.scroll = QScrollArea(widgetResizable=True)
        self.pdfviewer = PDFViewer(self)
        self.pdfviewer.setPalette(settings.app["palette"])
        self.scroll.setWidget(self.pdfviewer)
        self.layout().addWidget(self.scroll)
        self.invertPixels = False

        toolbar.init()

        def wrapper(f):
            def inner():
                toolbar.actions[f]['action'].trigger()
            return inner
        
        for f in ['zoomin','zoomout','fitW','fitH','invert']:
            setattr(self, f, wrapper(f))


    def load(self, path):
        self.pdfviewer.path = path
        self.pdfviewer.load()



