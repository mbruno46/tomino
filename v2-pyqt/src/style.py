from settings import get_theme

theme = get_theme()

def set_item(item, props):
    return f"{item} {{\n{props}}}"

editor_style = '\n'.join([
    set_item('QTabWidget::tab-bar', 'alignment: left;'),
    set_item('QTabWidget::pane', 'border: 0px'),
    set_item('QTabWidget Editor', 'border: 0px'),
    set_item('QTabBar::tab', f'padding: 0.8em; border: 0px; color: {theme["gray"]}'),
    set_item('QTabBar::tab:selected', f'background: {theme["text-background"]}; color: {theme["text"]}; border-top: 4px solid {theme["highlight"]};'),
    set_item('QTabBar::close-button', 'subcontrol-position: right;'),
])


browser_style = '\n'.join([
    # set_item('QTabWidget::tab-bar', 'alignment: left;'),
    # set_item('QTabBar::tab', f'padding: 0.8em; border: 0px; border-left: 4px solid; color: {theme["gray"]}'),
    # set_item('QTabBar::tab:selected', f'border-left: 4px solid {theme["highlight"]}'),
    set_item('Browser QToolBar', f'border: 0px'),
    set_item('Browser QToolBar QToolButton', f'background: {theme["app-background"]}; padding: 8px; border: 0px; border-left: 4px solid {theme["app-background"]}'),
    set_item('Browser QToolBar QToolButton:checked', f'border-left: 4px solid {theme["hover"]};')
])


viewer_style = '\n'.join([
    set_item('Viewer QPushButton',f'background: {theme["browser-background"]}; color: {theme["text"]}; border-radius: 8px; border: 1px solid;'),
    set_item('Viewer QPushButton', 'min-height: 2em; min-width: 2em;'),
    set_item('Viewer QPushButton:hover', f'background: {theme["hover"]}'),
    set_item('Viewer QPushButton:pressed', f'background: {theme["hover"]}; border: 2px solid;'),
])