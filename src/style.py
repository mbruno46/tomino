from settings import get_theme

theme = get_theme()

def set_item(item, props):
    return f"{item} {{\n{props}}}"

editor_style = '\n'.join([
    set_item('QTabWidget::tab-bar', 'alignment: left;'),
    set_item('QTabWidget::pane', 'border: 0px'),
    set_item('QTabWidget Editor', 'border: 0px'),
    set_item('QTabBar::tab', f'min-height: 3.2em; border: 0px; padding: -4px 0 0 4px; border-top: 4px solid {theme["app-background"]}; color: {theme["gray"]}'),
    set_item('QTabBar::tab:selected', f'background: {theme["text-background"]}; color: {theme["text"]}; padding: -4px 0 0 4px; border-top: 4px solid {theme["highlight"]};'),
    set_item('QTabBar::close-button', 'subcontrol-position: right;'),
])


browser_style = '\n'.join([
    set_item('Browser QToolBar', f'border: 0px;'),
    set_item('Browser QToolBar QToolButton', f'background: {theme["app-background"]}; padding: 8px; border: 0px; border-left: 4px solid {theme["app-background"]}'),
    set_item('Browser QToolBar QToolButton:checked', f'border-left: 4px solid {theme["hover"]};')
])


viewer_style = '\n'.join([
    # set_item('Viewer QPushButton',f'background: {theme["browser-background"]}; color: {theme["text"]}; border-radius: 8px; border: 1px solid;'),
    # set_item('Viewer QPushButton', 'min-height: 2em; min-width: 2em;'),
    # set_item('Viewer QPushButton:hover', f'background: {theme["hover"]}'),
    # set_item('Viewer QPushButton:pressed', f'background: {theme["hover"]}; border: 2px solid white;'),
    # set_item('Viewer', f'border-left: 2px solid {theme["app-background"]};'),
    # set_item('Viewer', 'margin-left: 4px solid;'),
    set_item('Viewer QScrollArea', f'border: 0px'),
    set_item('Viewer ToolBar', f'min-height: 3.2em; border: 0px;'),
    set_item('Viewer ToolBar QToolButton', 'padding: 4px; border-radius: 4px; margin-left: auto'),
    set_item('Viewer ToolBar QToolButton:hover', f'background: {theme["hover"]}'),
    # set_item('Viewer ToolBar QToolButton:pressed', f'background: {theme["hover"]}; border: 2px solid {theme["gray"]};'),
])

finder_style = '\n'.join([
    set_item('Finder', f'background: {theme["text-background"]}; border-top: 1px solid {theme["gray"]}'),
    set_item('Finder QLineEdit', f'background: {theme["browser-background"]}'),
    set_item('Finder QPushButton', f'background: transparent')
])

splitter_style = '\n'.join([
    set_item('QSplitter::handle:pressed', f'background: {theme["highlight"]}')
])