from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QToolButton, QToolBar, QStackedWidget
from PyQt6.QtWidgets import QPlainTextEdit, QListView, QStyledItemDelegate, QLabel, QSizePolicy
from PyQt6.QtGui import QIcon, QColorConstants, QImage, QPixmap, QPalette, QPainter, QBrush
from PyQt6.QtCore import QSize, Qt, QAbstractListModel, QModelIndex, QRectF
from PyQt6.QtSvg import QSvgRenderer

from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
# import pymupdf

from highligher import ErrorHighligther
import settings
import style
import svg

# import pyinstrument

svg_icons = {
    "Zoom In": '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M20 20L14.9497 14.9497M14.9497 14.9497C16.2165 13.683 17 11.933 17 10C17 6.13401 13.866 3 10 3C6.13401 3 3 6.13401 3 10C3 13.866 6.13401 17 10 17C11.933 17 13.683 16.2165 14.9497 14.9497ZM7 10H13M10 7V13" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>',
    "Zoom out": '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M20 20L14.9497 14.9498M14.9497 14.9498C16.2165 13.683 17 11.933 17 10C17 6.13401 13.866 3 10 3C6.13401 3 3 6.13401 3 10C3 13.866 6.13401 17 10 17C11.933 17 13.683 16.2165 14.9497 14.9498ZM7 10H13" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>',
    "Fit Width": '<svg viewBox="0 0 24 24" id="left-right-scroll-bar" data-name="Flat Line" xmlns="http://www.w3.org/2000/svg" class="icon flat-line"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><polyline id="primary" points="15 10 17 12 15 14" style="fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><polyline id="primary-2" data-name="primary" points="9 14 7 12 9 10" style="fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><path id="primary-3" data-name="primary" d="M21,6V18M3,6V18m14-6H7" style="fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></path></g></svg>',
    "Fit Height": '<svg viewBox="0 0 24 24" id="up-down-scroll-bar" data-name="Flat Line" xmlns="http://www.w3.org/2000/svg" class="icon flat-line"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><polyline id="primary" points="10 9 12 7 14 9" style="fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><polyline id="primary-2" data-name="primary" points="14 15 12 17 10 15" style="fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></polyline><path id="primary-3" data-name="primary" d="M6,3H18M6,21H18M12,7V17" style="fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2;"></path></g></svg>',
    "Invert colors": '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" d="M4,14 C4,11.0544813 6.66666667,7.05448133 12,2 C17.3333333,7.05448133 20,11.0544813 20,14 C20,18.3349143 16.5521622,21.8645429 12.2491793,21.9961932 L12,22 C7.581722,22 4,18.418278 4,14 Z M12,4.793 L11.7832437,5.01193635 C7.89798368,8.95774552 6,12.0287291 6,14 C6,17.3137085 8.6862915,20 12,20 L12,4.793 Z"></path> </g></svg>',
}


class PDFPageDelegate2(QStyledItemDelegate):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.r = QSvgRenderer()
        self.invert = False
        self.scale = 1.0
        self.page_size = None

    def zoom(self, incr):
        if incr and (self.scale<2.0):
            self.scale += 0.1
        if not incr and (self.scale>0.2):
            self.scale -= 0.1

    def fit(self, tag, val):
        if tag=='W':
            self.scale = val / self.page_size.width()
        elif tag=='H':
            self.scale = val / self.page_size.height()

    def paint(self, painter, option, index):
        # idx = index.data(Qt.DisplayRole)
        data_svg = index.data(Qt.UserRole+123)
        rect = QRectF(option.rect)
    
        if not self.invert:
            painter.fillRect(rect, QColorConstants.White)
        else:
            theme = settings.get_theme()
            data_svg = data_svg.replace('path id=', f'path fill="{theme["text"]}" id=')
        self.r.load(data_svg.encode('utf-8'))

        self.page_size = self.r.viewBox()
        rect.setWidth(rect.height() * self.page_size.width() / self.page_size.height())

        self.r.render(painter, rect)

    def sizeHint(self, option, index):
        data_svg = index.data(Qt.UserRole+123)
        self.r.load(data_svg.encode('utf-8'))
        r = self.r.viewBox()
        return QSize(int(r.width() * self.scale), int(r.height() * self.scale))


class PDFPageDelegate(QStyledItemDelegate):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.r = QSvgRenderer()
        self.invert = False
        self.scale = 1.0
        self.page_size = None

    def zoom(self, incr):
        if incr and (self.scale<2.0):
            self.scale += 0.1
        if not incr and (self.scale>0.2):
            self.scale -= 0.1

    def fit(self, tag, val):
        if tag=='W':
            self.scale = val / self.page_size.width()
        elif tag=='H':
            self.scale = val / self.page_size.height()

    def paint(self, painter, option, index):
        # idx = index.data(Qt.DisplayRole)
        data_svg = index.data(Qt.UserRole+123)
        rect = QRectF(option.rect)
    
        

    def sizeHint(self, option, index):
        data_svg = index.data(Qt.UserRole+123)
        self.r.load(data_svg.encode('utf-8'))
        r = self.r.viewBox()
        return QSize(int(r.width() * self.scale), int(r.height() * self.scale))


class PDFModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.pages = []
        
    def rowCount(self, index: QModelIndex):
        return len(self.pages)
    
    def data(self, index: QModelIndex, role):
        if index.isValid():
            if (role==Qt.DisplayRole):
                return index.row()
            elif (role==Qt.UserRole+123):
                return self.pages[index.row()]
        return None



class PDFViewer3(QListView):
    def __init__(self, parent = None):
        super().__init__(parent)
        # self.setPalette(settings.app["palette"])
        self.setSpacing(10)
        self.verticalScrollBar().setSingleStep(10)
        self.horizontalScrollBar().setSingleStep(20)

        self.pdfmodel = PDFModel()
        self.setModel(self.pdfmodel)
        self.path = None
        self.pdfpage = PDFPageDelegate(self)
        self.setItemDelegate(self.pdfpage)
    
        self.repaint = lambda : self.pdfmodel.layoutChanged.emit()

    def load(self):
        if self.path is None:
            return
        
        self.pdfmodel.pages = []
        doc = pymupdf.open(self.path)
        for i, p in enumerate(doc):
            page = p.get_pixmap()
            # page = page.replace('g clip-path','g fill="red" clip-path')
            # page = page.replace('clipPath id','clipPath fill="green" id')
            self.pdfmodel.pages.append(page)
        doc.close()
        self.repaint()

    def close(self):
        self.pdfmodel.pages = []
        self.repaint()

    def invert(self, bool):
        self.pdfpage.invert = bool
        self.repaint()

    def zoomin(self):
        self.pdfpage.zoom(True)
        self.repaint()

    def zoomout(self):
        self.pdfpage.zoom(False)
        self.repaint()

    def fitW(self):
        self.pdfpage.fit('W', self.width() - 20)
        self.repaint()

    def fitH(self):
        self.pdfpage.fit('H', self.height() - 20)
        self.repaint()


class PDFViewer(QPdfView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setPageSpacing(10)
        self.setPageMode(QPdfView.PageMode.MultiPage)

        palette = QPalette(settings.app["palette"])
        palette.setBrush(QPalette.ColorRole.Dark, settings.app["palette"].window())
        # palette.setBrush(QPalette.ColorRole.Dark, settings.app["palette"].ColorRole.Window())
        self.setPalette(palette)
        
        self.path = None
        self.scale = 1.0

    
    def load(self):
        if self.path is None:
            return
        
        doc = QPdfDocument(self)
        doc.load(self.path)
        self.setDocument(doc)

    def close(self):
        self.setDocument(None)

    def fitW(self):
        self.setZoomMode(QPdfView.ZoomMode.FitToWidth)

    def fitH(self):
        self.setZoomMode(QPdfView.ZoomMode.FitInView)

    def zoom(self, incr):
        self.setZoomMode(QPdfView.ZoomMode.Custom)
        if incr and (self.scale<2.0):
            self.scale += 0.1
        if not incr and (self.scale>0.2):
            self.scale -= 0.1
        self.setZoomFactor(self.scale)

    def zoomin(self):
        self.zoom(True)

    def zoomout(self):
        self.zoom(False)


class PDFError(QPlainTextEdit):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setPalette(settings.viewer["error"]["palette"])
        self.setFont(settings.viewer["error"]["font"])
        self.setReadOnly(True)

        self.highlighter = ErrorHighligther(self.document())
        

        
class Viewer(QWidget):
        
    class ToolBar(QToolBar):
        class ToolButton(QToolButton):
            def __init__(self, parent, icons, func):
                super().__init__(parent)
                self.icons = icons
                self.func = func
                self.setIcon(self.icons[0])
                self.pressed.connect(self(pressing=True))
                self.released.connect(self(pressing=False))
                
            def __call__(self, pressing):
                def inner():
                    self.setIcon(self.icons[1 if pressing else 0])
                    if not pressing:
                        self.func()
                return inner


        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.setOrientation(Qt.Orientation.Horizontal)
            self.setIconSize(QSize(32, 32))
            self.setPalette(settings.app["palette"])
            # self.layout().setAlignment(Qt.AlignRight)
            # self.setAllowedAreas(Qt.RightToolBarArea)
            self.policy = QSizePolicy()
            self.policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
            

        def init(self):
            theme = settings.get_theme()

            self.actions = {}
            for key, func  in zip(
                ["Zoom In", "Zoom out", "Fit Width", "Fit Height"], 
                ['zoomin', 'zoomout', 'fitW',  'fitH']):

                icons = []
                for c, s in zip(['gray', 'text'], [QIcon.State.Off, QIcon.State.On]):
                    icons += [svg.create_icon(svg_icons[key],("stroke", theme[c]))]

                b = self.ToolButton(self, icons, getattr(self.parent.pdfviewer, func))
                b.setSizePolicy(self.policy)
                self.addWidget(b)
                self.actions[func] = b

            # key = "Invert colors"

            # icon = QIcon()
            # for c, s in zip(['gray', 'text'], [QIcon.State.Off, QIcon.State.On]):
            #     ico = svg.create_icon(svg_icons[key],("stroke", theme[c]),("fill", theme[c]))
            #     icon.addPixmap(ico.pixmap(QSize(32,32)), QIcon.Mode.Active, s)

            # b = QToolButton(self)
            # b.setCheckable(True)
            # b.clicked.connect(self.invert)
            # b.setIcon(icon)
            # self.addWidget(b)
            # self.actions['invert'] = b
            # b.click()

        def invert(self):
            pass
        #     w = self.sender()
        #     if w:
        #         self.parent.pdfviewer.invert(not w.isChecked())
                  

    def __init__(self, app):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet(style.viewer_style)
        self.layout().setContentsMargins(4,0,0,0)
        self.layout().setSpacing(0)

        toolbar = self.ToolBar(self)
        self.layout().addWidget(toolbar)

        self.scroll = QScrollArea(widgetResizable=True)
        self.pdfviewer = PDFViewer(None)
        self.scroll.setWidget(self.pdfviewer)


        #doc = pymupdf.open('/Users/mbruno/Physics/tomino/dummy/main.pdf')
        #pix = doc[0].get_pixmap()#alpha=False, dpi=72)
        #fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        #qtimg = QImage(pix.samples_ptr, pix.width, pix.height, pix.stride, fmt)
        #qtpix = QPixmap.fromImage(qtimg)
        #l = QLabel()
        #l.setPixmap(qtpix) #, Qt.NoFormatConversion))
        #doc.close()

        # self.scroll.setWidget(self.pdfviewer)

        self.errmsg = PDFError(self)

        self.panel = QStackedWidget()
        self.panel.addWidget(self.scroll)
        self.panel.addWidget(self.errmsg)
        self.layout().addWidget(self.panel)
        
        toolbar.init()

        def wrapper(f):
            def inner():
                toolbar.actions[f].click()
            return inner
        
        for f in ['zoomin','zoomout','fitW','fitH']:#,'invert']:
            setattr(self, f, wrapper(f))

    def load(self, path):
        self.pdfviewer.path = path
        self.pdfviewer.load()
        self.panel.setCurrentIndex(0)

    def show_err(self, logfile):
        self.panel.setCurrentIndex(1)
        with open(logfile, 'r') as f:
            self.errmsg.setPlainText(f.read())

    def close(self):
        self.pdfviewer.close()
        self.panel.setCurrentIndex(0)
