from PyQt5.QtWidgets import QGroupBox, QLineEdit, QLabel, QGridLayout, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor

import svg
import style
import settings

svg_icon = {
    'up': '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M6 15L12 9L18 15" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>',
    'down': '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <rect width="24" height="24" fill="white"></rect> <path d="M17 9.5L12 14.5L7 9.5" stroke="#000000" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>',
}

class Finder(QGroupBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setStyleSheet(style.finder_style)
        theme = settings.get_theme()

        layout= QGridLayout()

        label = QLabel('Find', self)
        label.setFont(settings.editor["font"])
        # label.setForegroundRole(QColor(theme["gray"]))
        layout.addWidget(label,0,0)

        self.find = QLineEdit()
        self.find.setFont(settings.editor["font"])
        layout.addWidget(self.find,0,1)

        next = QPushButton()
        next.setIcon(svg.create_icon(svg_icon['up'], ("stroke", theme['gray'])))
        sz = self.fontMetrics().height() * 2
        next.setFixedSize(QSize(sz,sz))
        next.clicked.connect(lambda x: parent.file_editor.find(self.find.text(), False))
        layout.addWidget(next,0,2)

        prev = QPushButton('<')
        prev.clicked.connect(lambda x: parent.file_editor.find(self.find.text(), True))
        layout.addWidget(prev,0,3)

        self.setLayout(layout)
        self.setVisible(False)

    def toggle(self):
        self.setVisible(not self.isVisible())
        self.find.setFocus()

    
