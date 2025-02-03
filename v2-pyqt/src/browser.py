from PyQt5.QtWidgets import QTreeWidget, QStyle, QStyleOptionTabV4, QStylePainter, QTreeWidgetItem, QTabWidget, QTabBar, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPainter, QIcon, QPixmap
from PyQt5.QtCore import QSize, QRect, QPoint
import glob, os

import settings
import style
import autocompleter

def build_tree(parent, path):
    item = Item(parent, path)
    for f in glob.glob(f"{path}/*"):
        build_tree(item, f)

class FileDatabase:
    def __init__(self):
        self.tex = []
        self.bib = []
        pass

    def init(self, root):
        self.root = root
        self.tex = []
        self.bib = []

    def add(self, filename):
        rel_path = os.path.relpath(filename, self.root)
        # base = os.path.basename(filename)
        ext = os.path.splitext(filename)[1]
        if ext=='.tex':
            self.tex.append(rel_path)

file_database = FileDatabase()

class Item(QTreeWidgetItem):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.setText(0, os.path.basename(path))
        self.path = path
        self.is_file = os.path.isfile(path)
        if self.is_file:
            file_database.add(path)

    def setMainTex(self, condition):
        if condition:
            self.setForeground(0, settings.browser["palette"].brightText())
        else:
            self.setBackground(0, settings.browser["palette"].base())

class FileBrowser(QTreeWidget):
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.setPalette(settings.browser["palette"])

        self.itemClicked.connect(self.onItemClicked)
        self.doubleClicked.connect(self.setMainTex)
        self.setHeaderHidden(True)
        self.setAnimated(True)

        self.main_index = None
        
    def load(self, path):
        self.path = path
        self.clear()
        self.app.file_editor.clear()
        file_database.init(path)

        build_tree(self, path)
        if self.topLevelItemCount()==1:
            self.topLevelItem(0).setExpanded(True)
        
        autocompleter.input = file_database.tex
        print(file_database.__dict__)
        
    def onItemClicked(self, item, col):
        if item.is_file:
            self.app.file_editor.load_file(item.path)

    def setMainTex(self, index):
        item = self.itemFromIndex(index)
        if item.is_file:
            if not self.main_index is None:
                old_item = self.itemFromIndex(self.main_index)
                old_item.setMainTex(False)
            self.main_index = index
            item.setMainTex(True)
            self.app.main_tex_file = item.path

            autocompleter.parser.main = item.path
            autocompleter.parser()
            
# class Browser(QWidget):
#     def __init__(self, app):
#         super().__init__(app)
#         self.setLayout(QHBoxLayout())
#         self.setStyleSheet(style.browser_style)

#         toolbar = QWidget()
#         toolbar.setLayout(QVBoxLayout())
#         for icon, paneidx in [
#             ('files', 0),
#             ('two', 1)
#         ]:
#             btn = QPushButton()
#             btn.setText(icon)
#             btn.clicked.connect(self.switch_layout(paneidx))
#             toolbar.layout().addWidget(btn)
#         self.layout().addWidget(toolbar)

#         self.browser = QStackedWidget()
#         self.file_browser = FileBrowser(app)
#         self.browser.addWidget(self.file_browser)
#         lab = QLabel("sad")
#         self.browser.addWidget(lab)
#         self.layout().addWidget(self.browser)

#     def switch_layout(self, idx):
#         def inner(arg):
#             self.browser.setCurrentIndex(idx)
#         return inner
    
#     def load(self, path):
#         self.file_browser.load(path)

class Browser(QTabWidget):
    class TabBar(QTabBar):
        def __init__(self, panel):
            super().__init__()
            self.panel = panel

        def tabSizeHint(self, index):
            s = QTabBar.tabSizeHint(self, index)
            s.transpose()
            self.panel.setContentsMargins(s.width(), 0, 0, 0)
            return s
        
        def paintEvent(self, event):
            painter = QStylePainter(self)
            opt = QStyleOptionTabV4()

            for i in range(self.count()):
                self.initStyleOption(opt, i)
                painter.drawItemPixmap(opt.rect, 0, QPixmap("images.png"))

            # for i in range(self.count()):
            #     self.initStyleOption(opt, i)
            #     painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            #     painter.save()

            #     s = opt.rect.size()
            #     s.transpose()

            #     r = QRect(QPoint(), s)
            #     r.moveCenter(opt.rect.center())
            #     opt.rect = r

            #     c = self.tabRect(i).center()
            #     painter.translate(c)
            #     painter.rotate(90)
            #     painter.translate(-c)
            #     # painter.drawControl(QStyle.CE_TabBarTabLabel,opt)
            #     painter.drawItemPixmap(opt.rect, 0, QPixmap("images.png"))
            #     painter.restore()
                
        # def paintEvent(self, a0):
        #     painer = QStylePainter(self)
        #     return super().paintEvent(a0)
    def __init__(self, app):
        super().__init__()
        self.setStyleSheet(style.browser_style)
        self.setTabBar(self.TabBar(self))

        self.setTabPosition(QTabWidget.West)
        self.file_browser = FileBrowser(app)
        self.addTab(self.file_browser, QIcon("images.png"), "")
        lab = QLabel("sad")
        self.addTab(lab, QIcon("images.png"), "")

    def load(self, path):
        self.file_browser.load(path)
