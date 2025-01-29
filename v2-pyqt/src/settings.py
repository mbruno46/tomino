from PyQt5.QtGui import QFont, QFontDatabase, QColor, QPalette
# from PyQt5.QtGui import QIcon, QPixmap
# import glob, os
# icons = {}
# for f in glob.glob("icons/*"):
#     icons[os.path.basename(f)] = QIcon(QPixmap(f))

app = {}
editor = {}
browser = {}

theme = {
    "dark": {
        "app-background": "#1c1f26",
        "text-background": "#232830",
        "browser-background": "#2b303b",
        "text": "#dfe1e8",
        "highlight": "#1f4b70",
        "border": "#333d46",
        "green": '#a6e86d',
        "command": "#82c448",
        "square": "#f1727f",
        "curly": "#ff84e8",
        "comment": "#5d90c4",

    }
}

def init():
    global editor

    id = QFontDatabase.addApplicationFont('/Users/mbruno/Physics/tomino/v2-pyqt/src/assets/source-code-pro/SourceCodePro-Regular.ttf')
    families = QFontDatabase.applicationFontFamilies(id)

    palette = QPalette()
    palette.setColor(QPalette.Highlight, QColor(theme['dark']['highlight']))
    palette.setColor(QPalette.Text, QColor(theme['dark']['text']))
    palette.setColor(QPalette.HighlightedText, QColor(theme['dark']['text']))
    palette.setColor(QPalette.WindowText, QColor(theme['dark']['text']))

    editor["font"] = QFont(families[0], 14)
    editor["palette"] = QPalette(palette)
    editor["palette"].setColor(QPalette.Base, QColor(theme['dark']['text-background']))

    app["palette"] = QPalette(palette)
    app["palette"].setColor(QPalette.Window, QColor(theme['dark']['app-background']))

    browser["palette"] = QPalette(palette)
    browser["palette"].setColor(QPalette.Base, QColor(theme['dark']['browser-background']))
