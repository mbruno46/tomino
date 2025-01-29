from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from vpanel import VPanel

class Browser(VPanel):
    def __init__(self, parent):
        super().__init__(parent)

        tree = QTreeWidget()
        
        parent = QTreeWidgetItem(tree)
        parent.setText(0, "parent")
        for i in range(5):
            child = QTreeWidgetItem(parent)
            child.setText(0, f"child {i}")

        self.layout.addWidget(tree)