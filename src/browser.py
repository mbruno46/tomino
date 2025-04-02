from PyQt6.QtWidgets import QStackedWidget,QToolBar, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTreeView
from PyQt6.QtGui import QFont, QFileSystemModel, QAction
from PyQt6.QtCore import QSize, Qt, QModelIndex

import os, sys

import settings
import style
import autocompleter
import svg
import latex

svg_icons = {
    'Explorer': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"></path> <path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"></path> <path d="M15 2v5h5"></path> </g></svg>',
    'Document': '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M8 8H20M11 12H20M14 16H20M4 8H4.01M7 12H7.01M10 16H10.01" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>'
}


class FileBrowserTree(QTreeView):
    class FileSystemModel(QFileSystemModel):
        def __init__(self, parent = None):
            self.main = ''
            super().__init__(parent)

        def setMain(self, index):
            self.main = self.filePath(index)
            self.dataChanged.emit(QModelIndex(), QModelIndex())

        def data(self, index, role = Qt.ItemDataRole.DisplayRole):
            if (self.main == self.filePath(index)) and (role == Qt.ItemDataRole.FontRole):
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
        
        self.clicked.connect(self.onClick)
        self.doubleClicked.connect(self.onDoubleClick)
        
    def load(self, path):
        self.fsm = self.FileSystemModel()
        self.fsm.setNameFilters(["*.tex","*.bib"] + [f"*{e}" for e in self.allowed_figures])
        self.fsm.setNameFilterDisables(False)
        self.fsm.rowsInserted.connect(self.onRowsInserted)
        self.fsm.rowsAboutToBeRemoved.connect(self.onRowsRemoved)
        self.setModel(self.fsm)

        for i in [1,2,3]:
            self.hideColumn(i)
        self.setHeaderHidden(True)

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

        return ext

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
        if index.isValid():
            if not index.internalPointer().parent.parent is None:
                fn, ln = index.internalPointer().location
                self.app.file_editor.focus_on_line(fn, ln)


class Browser(QWidget):
    class ToolBar(QToolBar):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.setOrientation(Qt.Orientation.Vertical)
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

        self.toolbar = self.ToolBar(self)
        self.layout().addWidget(self.toolbar)

        self.browser = QStackedWidget()
        self.file_browser = FileBrowserTree(app)
        self.browser.addWidget(self.file_browser)
        self.toc = TOC(app)        
        self.browser.addWidget(self.toc)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(settings.browser["font"])

        self.vpanel = QWidget()
        self.vpanel.setPalette(settings.browser["palette"])
        self.vpanel.setAutoFillBackground(True)
        self.vpanel.setLayout(QVBoxLayout())
        self.vpanel.layout().setContentsMargins(0,0,0,0)
        self.vpanel.layout().addSpacing(10)
        self.vpanel.layout().addWidget(self.label)
        self.vpanel.layout().addWidget(self.browser)

        self.layout().addWidget(self.vpanel)

        self.toolbar.switch_tab(0)
    
    def toggle_visibility(self, width):
        w = self.toolbar.width() if self.vpanel.isVisible() else width
        self.vpanel.setVisible(not self.vpanel.isVisible())
        self.setFixedWidth(w)
    
    def load(self, path):
        self.file_browser.load(path)
        self.label.setText(os.path.basename(path))

