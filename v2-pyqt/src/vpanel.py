from PyQt5.QtWidgets import QVBoxLayout, QWidget


class VPanel:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.main = QWidget()
        self.main.setLayout(self.layout)
        
    def __call__(self):
        return self.main