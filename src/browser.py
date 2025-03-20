from PyQt5.QtWidgets import QSizePolicy, QTreeWidget, QStackedWidget,QToolBar, QAction, QToolButton,  QStyleOptionTabV4, QStylePainter, QTreeWidgetItem, QTabWidget, QTabBar, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFileSystemModel, QTreeView
from PyQt5.QtGui import QPainter, QIcon, QPixmap, QIconEngine, QImage, QFont, QColor
from PyQt5.QtCore import QSize, QRect, QPoint, Qt, QModelIndex, QAbstractItemModel, QFileSystemWatcher, QRegExp, pyqtSlot
from PyQt5.QtSvg import QSvgWidget

import glob, os, sys

import settings
import style
import autocompleter
import svg
import latex

svg_icons = {
    'Explorer': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"></path> <path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"></path> <path d="M15 2v5h5"></path> </g></svg>',
    'Document': '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M8 8H20M11 12H20M14 16H20M4 8H4.01M7 12H7.01M10 16H10.01" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>'
}

# def build_tree(parent, path):
#     item = Item(parent, path)
#     if item.is_file:
#         ext = file_database.add(path)
#         if ext is None:
#             item.parent().removeChild(item)
#         item.set_ext(ext)
#         return
#     for f in sorted(glob.glob(f"{path}/*")):
#         build_tree(item, f)

# class FileDatabase:
#     def __init__(self):
#         pass

#     def init(self, root):
#         self.root = root
#         self.tex = []
#         self.bib = []
#         self.figures = []

#     def add(self, filename):
#         rel_path = os.path.relpath(filename, self.root)
#         # base = os.path.basename(filename)
#         ext = os.path.splitext(filename)[1]
#         if ext=='.tex':
#             self.tex.append(rel_path)
#         elif ext=='.bib':
#             self.bib.append(rel_path) 
#         elif ext in ('.pdf','.eps','.png','.jpg'):
#             self.figures.append(rel_path)
#         else:
#             ext = None
#         return ext

# file_database = FileDatabase()

# class Item(QTreeWidgetItem):
#     def __init__(self, parent, path):
#         super().__init__(parent)
#         self.setText(0, os.path.basename(path))
#         self.path = path
#         self.is_file = os.path.isfile(path)

#     def set_ext(self, ext):
#         self.extension = ext

#     @property
#     def is_tex(self):
#         return self.extension == '.tex'
    
#     def setMainTex(self, condition):
#         if condition:
#             self.setForeground(0, settings.browser["palette"].brightText())
#         else:
#             self.setForeground(0, settings.browser["palette"].text())

# class FileBrowser2(QTreeWidget):
#     def __init__(self, app):
#         self.app = app
#         super().__init__()
#         self.setPalette(settings.browser["palette"])
#         self.setFont(settings.browser["font"])
        
#         self.itemClicked.connect(self.onItemClicked)
#         self.doubleClicked.connect(self.setMainTex)
#         self.setHeaderHidden(True)
#         self.setAnimated(True)

#         self.main_index = None
        
#     def load(self, path):
#         self.path = path
#         self.clear()
#         self.app.file_editor.clear()
#         file_database.init(path)

#         build_tree(self, path)
#         if self.topLevelItemCount()==1:
#             self.topLevelItem(0).setExpanded(True)
        
#         autocompleter.input = file_database.tex
#         print(file_database.__dict__)
        
#     def onItemClicked(self, item: Item, col):
#         if item.is_file:
#             if item.is_tex:
#                 self.app.file_editor.load_file(item.path)

#     def setMainTex(self, index):
#         item = self.itemFromIndex(index)
#         if item.is_file and item.is_tex:
#             if not self.main_index is None:
#                 old_item = self.itemFromIndex(self.main_index)
#                 old_item.setMainTex(False)
#             self.main_index = index
#             item.setMainTex(True)
#             self.app.main_tex_file = item.path

#             autocompleter.parser.main = item.path
#             autocompleter.parser()




class FileBrowserTree(QTreeView):
    class FileSystemModel(QFileSystemModel):
        def __init__(self, parent = None):
            self.main = ''
            super().__init__(parent)

        def setMain(self, index):
            self.main = self.filePath(index)
            self.dataChanged.emit(QModelIndex(), QModelIndex())

        def data(self, index, role = Qt.DisplayRole):
            if (self.main == self.filePath(index)) and (role == Qt.FontRole):
                font = QFont()
                font.setUnderline(True)
                return font
            return super().data(index, role)

    def __init__(self, app = None):
        self.app = app
        super().__init__(app)
        self.setPalette(settings.browser["palette"])
        self.setFont(settings.browser["font"])

        self.allowed_figures = ['.pdf','.eps','.png','.jpg']
        self.fsm = self.FileSystemModel()
        self.fsm.setNameFilters(["*.tex","*.bib"] + [f"*{e}" for e in self.allowed_figures])
        self.fsm.setNameFilterDisables(False)
        self.fsm.rowsInserted.connect(self.onRowsInserted)
        self.fsm.rowsAboutToBeRemoved.connect(self.onRowsRemoved)
        self.setModel(self.fsm)
        
        for i in [1,2,3]:
            self.hideColumn(i)
        self.setHeaderHidden(True)

        self.clicked.connect(self.onClick)
        self.doubleClicked.connect(self.onDoubleClick)

        # self.watcher = QFileSystemWatcher()
        # self.watcher.fileChanged.connect(self.onFileChanged)
        
    def load(self, path):
        self.root = path
        self.files = {}

        self.fsm.setRootPath(path)
        self.setRootIndex(self.fsm.index(path))
        
    def update(self, filename, remove):
        rel_path = os.path.relpath(filename, self.root)
        ext = os.path.splitext(filename)[1]
        if ext=='.tex':
            autocompleter.input.update_keyword(rel_path, remove)
        elif ext=='.bib':
            autocompleter.bibliography.update_keyword(rel_path, remove)
        elif ext in self.allowed_figures:
            autocompleter.includegraphics.update_keyword(rel_path, remove)
        else:
            ext = None

        # if ext in ('.tex', '.bib'):
        #     if remove:
        #         del self.files[filename]
        #         # self.watcher.removePath(filename)
        #     else:
        #         cls = latex.TexFile if ext=='.tex' else latex.BibFile
        #         self.files[filename] = cls(filename)
        #         # self.watcher.addPath(filename)

        return ext
    

    # def onFileChanged(self, path):
    #     if not os.path.exists(path):
    #         # file removal or renamed handled by rowsremoved
    #         return

    #     if path in self.files:
    #         self.files[path]()


    def onRowsInserted(self, idx, i0, i1):
        for i in range(i0, i1+1):
            _idx = self.fsm.index(i, 0, idx)
            self.update(self.fsm.filePath(_idx), remove=False)
        
    def onRowsRemoved(self, idx, i0, i1):
        for i in range(i0, i1+1):
            _idx = self.fsm.index(i, 0, idx)
            fn = self.fsm.filePath(_idx)
            self.update(fn, remove=True)
            self.app.file_editor.file_obsolete(fn)
            
    def editable(self, index, texonly):
        if not self.fsm.isDir(index):
            path = self.fsm.filePath(index)
            ext = os.path.splitext(path)[1]
            if texonly:
                return ext==".tex"
            if ext in (".tex", ".bib"):
                return True
        return False
    

    def onClick(self, index):
        if self.editable(index, texonly=False):
            self.app.file_editor.load_file(self.fsm.filePath(index))

    def onDoubleClick(self, index: QModelIndex):        
        if self.editable(index, texonly=True):
            path = self.fsm.filePath(index)
            self.app.main_tex_file = path
            latex.init(path)
            self.app.browser.toc.expandAll()
            self.fsm.setMain(index)
        else:
            if sys.platform == 'darwin':
                os.popen(f'open {self.fsm.filePath(index)}')

    # def parse_main(self, filename):
    #     # root = os.path.dirname(filename)
    #     self.files = [latex.TexFile(filename)]
    #     for fn in self.files[0].data['input']:
    #         self.files += [latex.TexFile(fn)]
        
    # def parse_main_0(self, filename):
    #     text = open(filename, 'r').read()

    #     for f in self.files.values():
    #         f.setLinked(False)
    #     self.files[filename].setLinked(True)
    #     root = os.path.dirname(filename)

    #     for keyword in ['input', 'bibliography']:
    #         re = QRegExp("\\\\%s\\{(.*)\\}" % keyword)
    #         re.setMinimal(True)
    #         index = re.indexIn(text)

    #         print(re)
    #         while index >= 0:
    #             word = re.cap(1)
    #             for w in word.split(','):
    #                 fn = os.path.join(root, w)
    #                 if fn in self.files:
    #                     self.files[fn].setLinked(True)
    #             index = re.indexIn(text, index + 9 + len(word))

    #     for f in self.files.values():
    #         f()


class FileBrowser(QWidget):
    def __init__(self, app):
        super().__init__(app)
        self.setPalette(settings.browser["palette"])
        self.setAutoFillBackground(True)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,10,0,10)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(settings.browser["font"])
        self.layout().addWidget(self.label)

        self.file_browser = FileBrowserTree(app)
        self.layout().addWidget(self.file_browser)

    def load(self, path):
        self.file_browser.load(path)
        self.label.setText(os.path.basename(path))


class TOC(QTreeView):
    def __init__(self, app = None):
        self.app = app
        super().__init__(app)
        self.setPalette(settings.browser["palette"])
        self.setFont(settings.browser["font"])

        self.setHeaderHidden(True)
        self.setModel(latex.model)

        self.doubleClicked.connect(self.onDoubleClick)

    def onDoubleClick(self, index: QModelIndex):
        fn, ln = index.internalPointer().location
        self.app.file_editor.focus_on_line(fn, ln)


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

        self.file_browser = FileBrowser(app)

        # lab = QLabel("Not implemented")
        w = QWidget()
        w.setPalette(settings.browser["palette"])
        w.setAutoFillBackground(True)

        w.setLayout(QVBoxLayout())
        w.layout().setContentsMargins(0,0,0,0)
        w.layout().addSpacing(20)
        self.toc = TOC(app)        
        w.layout().addWidget(self.toc)

        self.browser = QStackedWidget()
        self.browser.addWidget(self.file_browser)
        self.browser.addWidget(w)
        self.layout().addWidget(self.browser)

        toolbar.switch_tab(0)
    
    def load(self, path):
        self.file_browser.load(path)

