from PyQt5.QtWidgets import QLabel, QScrollArea
# from PyQt5.QtWeb import QWebEngineView , QWebEngineSettings
from PyQt5.QtGui import QImage, QPixmap
import pymupdf

from vpanel import VPanel
# import settings

class Viewer(VPanel):
    def __init__(self, app):
        super().__init__()
        self.scroll = QScrollArea()
        self.layout.addWidget(self.scroll)
    
    def load(self):
        path = "/Users/mbruno/Physics/ToM/dummy/main3.pdf"
        doc = pymupdf.open(path)
        page = doc[0] 
        pix = page.get_pixmap()

        # set the correct QImage format depending on alpha
        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        qimage = QImage(pix.samples_ptr, pix.width, pix.height, fmt)
        # qimage.invertPixels()
        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap.fromImage(qimage))

        self.scroll.setWidget(imageLabel)


