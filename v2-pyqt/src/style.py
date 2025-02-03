from settings import get_theme

theme = get_theme()

def set_item(item, props):
    return f"{item} {{\n{props}}}"

editor_style = '\n'.join([
    set_item('QTabWidget::tab-bar', 'alignment: left;'),
    set_item('QTabWidget::pane', 'border: 0px'),
    set_item('QTabWidget Editor', 'border: 0px'),
    set_item('QTabBar::tab', f'padding: 0.8em; border: 0px; color: {theme["gray"]}'),
    set_item('QTabBar::tab:selected', f'background: {theme["text-background"]}; color: {theme["text"]}; border-top: 4px solid {theme["highlight"]}'),
    set_item('QTabBar::close-button', 'subcontrol-position: right;'),
])

browser_style = '\n'.join([
    set_item('QTabWidget::tab-bar', 'alignment: left;'),
    set_item('QTabBar::tab', f'padding: 0.8em; border: 0px; color: {theme["gray"]}'),
    set_item('QTabBar::tab:selected', f'border-top: 4px solid {theme["highlight"]}'),
])