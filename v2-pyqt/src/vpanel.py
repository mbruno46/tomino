from PyQt5.QtWidgets import QVBoxLayout, QWidget


class VPanel:
    def __init__(self, parent):
        self.layout = QVBoxLayout(parent)
        self.main = QWidget()
        self.main.setLayout(self.layout)
        
    def __call__(self):
        return self.main