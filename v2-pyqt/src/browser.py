from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
import glob, os

from vpanel import VPanel
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

class Browser(QTreeWidget):
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.setPalette(settings.browser["palette"])

        self.itemClicked.connect(self.onItemClicked)
        self.setHeaderHidden(True)
        self.setAnimated(True)

    def init(self, path):
        self.path = path
        self.children = []
        build_tree(self, path)

    def onItemClicked(self, item, col):
        if item.is_file:
            self.app.editor.load_file(item.path)


class BrowserPanel(VPanel):
    def __init__(self, app):
        self.path = ""

        super().__init__()
        self.tree = Browser(app)
        self.layout.addWidget(self.tree)

        self.tree.init("/Users/mbruno/Physics/tomino/dummy")
