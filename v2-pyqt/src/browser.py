from PyQt5.QtWidgets import QTreeWidget, QStackedWidget,QToolBar, QAction, QToolButton,  QStyleOptionTabV4, QStylePainter, QTreeWidgetItem, QTabWidget, QTabBar, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPainter, QIcon, QPixmap, QIconEngine, QImage
from PyQt5.QtCore import QSize, QRect, QPoint, Qt
from PyQt5.QtSvg import QSvgWidget

import glob, os

import settings
import style
import autocompleter
import svg

svg_icons = {
    'Explorer': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"></path> <path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"></path> <path d="M15 2v5h5"></path> </g></svg>',
    'Document': '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M8 8H20M11 12H20M14 16H20M4 8H4.01M7 12H7.01M10 16H10.01" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>'
}

def build_tree(parent, path):
    item = Item(parent, path)
    if item.is_file:
        ext = file_database.add(path)
        if ext is None:
            item.parent().removeChild(item)
        item.set_ext(ext)
        return
    for f in sorted(glob.glob(f"{path}/*")):
        build_tree(item, f)

class FileDatabase:
    def __init__(self):
        pass

    def init(self, root):
        self.root = root
        self.tex = []
        self.bib = []
        self.figures = []

    def add(self, filename):
        rel_path = os.path.relpath(filename, self.root)
        # base = os.path.basename(filename)
        ext = os.path.splitext(filename)[1]
        if ext=='.tex':
            self.tex.append(rel_path)
        elif ext=='.bib':
            self.bib.append(rel_path) 
        elif ext in ('.pdf','.eps','.png','.jpg'):
            self.figures.append(rel_path)
        else:
            ext = None
        return ext

file_database = FileDatabase()

class Item(QTreeWidgetItem):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.setText(0, os.path.basename(path))
        self.path = path
        self.is_file = os.path.isfile(path)

    def set_ext(self, ext):
        self.extension = ext

    @property
    def is_tex(self):
        return self.extension == '.tex'
    
    def setMainTex(self, condition):
        if condition:
            self.setForeground(0, settings.browser["palette"].brightText())
        else:
            self.setForeground(0, settings.browser["palette"].text())

class FileBrowser(QTreeWidget):
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.setPalette(settings.browser["palette"])
        font = self.font()
        font.setPointSize(settings.editor["font"].pointSize())
        self.setFont(font)
        
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
        
    def onItemClicked(self, item: Item, col):
        if item.is_file:
            if item.is_tex:
                self.app.file_editor.load_file(item.path)

    def setMainTex(self, index):
        item = self.itemFromIndex(index)
        if item.is_file and item.is_tex:
            if not self.main_index is None:
                old_item = self.itemFromIndex(self.main_index)
                old_item.setMainTex(False)
            self.main_index = index
            item.setMainTex(True)
            self.app.main_tex_file = item.path

            autocompleter.parser.main = item.path
            autocompleter.parser()
            
class TeXBrowser(QTreeWidget):
    def  __init__(self, parent = ...):
        super().__init__(parent)


class Browser(QWidget):
    class ToolBar(QToolBar):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.setOrientation(Qt.Vertical)
            self.setPalette(settings.app["palette"])
            self.setIconSize(QSize(42,42))
            
            theme = settings.get_theme()

            self.icons = []
            self.actions = []
            for key in svg_icons:
                self.icons += [[
                    svg.create_icon(svg_icons[key], ("stroke", theme['gray'])),
                    svg.create_icon(svg_icons[key], ("stroke", theme['text']))
                ]]
                btn = QAction(key, self)
                btn.setCheckable(True)
                btn.setIcon(self.icons[-1][0])

                self.actions.append(btn)
                self.addAction(btn)

            self.actionTriggered.connect(self.trigger)
            self.active = 0
            


        def trigger(self, action):
            self.actions[self.active].setChecked(False)
            self.actions[self.active].setIcon(self.icons[self.active][0])

            idx = self.actions.index(action)
            self.parent.browser.setCurrentIndex(idx)
            self.active = idx

            action.setChecked(True)
            action.setIcon(self.icons[idx][1])            

        def switch_tab(self, idx):
            self.trigger(self.actions[idx])

    def __init__(self, app):
        super().__init__(app)
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        self.setStyleSheet(style.browser_style)

        toolbar = self.ToolBar(self)
        self.layout().addWidget(toolbar)

        self.browser = QStackedWidget()
        self.file_browser = FileBrowser(app)
        self.browser.addWidget(self.file_browser)
        lab = QLabel("Not implemented")
        self.browser.addWidget(lab)
        self.layout().addWidget(self.browser)

        toolbar.switch_tab(0)
    
    def load(self, path):
        self.file_browser.load(path)

