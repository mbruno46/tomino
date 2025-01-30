from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout
import glob, os

import settings

def build_tree(parent, path):
    item = Item(parent, path)
    for f in glob.glob(f"{path}/*"):
        build_tree(item, f)


class Item(QTreeWidgetItem):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.setText(0, os.path.basename(path))
        self.path = path
        self.is_file = os.path.isfile(path)

    def setMainTex(self, condition):
        if condition:
            self.setForeground(0, settings.browser["palette"].brightText())
        else:
            self.setBackground(0, settings.browser["palette"].base())

class Browser(QTreeWidget):
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.setPalette(settings.browser["palette"])

        self.itemClicked.connect(self.onItemClicked)
        self.doubleClicked.connect(self.setMainTex)
        self.setHeaderHidden(True)
        self.setAnimated(True)

        self.main_index = None

    def init(self, path):
        self.path = path
        self.clear()
        self.app.editor.clear()
        build_tree(self, path)
        if self.topLevelItemCount()==1:
            self.topLevelItem(0).setExpanded(True)

    def onItemClicked(self, item, col):
        if item.is_file:
            self.app.editor.load_file(item.path)

    def setMainTex(self, index):
        item = self.itemFromIndex(index)
        if item.is_file:
            if not self.main_index is None:
                old_item = self.itemFromIndex(self.main_index)
                old_item.setMainTex(False)
            self.main_index = index
            item.setMainTex(True)
            self.app.main_tex_file = item.path

class BrowserPanel(QWidget):
    def __init__(self, app):
        self.app = app

        super().__init__()
        self.browser = Browser(app)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.browser)

        self.browser.init("/Users/mbruno/Physics/tomino/dummy")

    def open_folder(self, path):
        self.browser.init(path)