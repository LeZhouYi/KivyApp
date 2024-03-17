from kivy.core.window import Window
from kivy.uix.widget import Widget

from screeninfo import get_monitors


def create_key(base_key: str, *args):
    """构建控件Key"""
    for value in args:
        base_key = "%s_%s" % (base_key, str(value))
    return base_key


def event_adaptor(method, **kwargs):
    """为控件事件实现带参数方法"""
    return lambda event, fun=method, params=kwargs: fun(event, **params)


def calculate_height(widget: Widget) -> float:
    """计算控件显示的最小高度"""
    child_amount = len(widget.children)
    child_height_all = 0
    for child_widget in widget.children:
        child_height_all += child_widget.height
    padding_offset = widget.padding[1] + widget.padding[3]
    spacing_offset = 0 if child_amount <= 1 else widget.spacing * (child_amount - 1)
    return child_height_all + padding_offset + spacing_offset


def set_center_window(width: int, height: int):
    """设置窗口宽高并居中"""
    monitors = get_monitors()
    screen_width = monitors[0].width
    screen_height = monitors[0].height
    x = (screen_width - width) // 4
    y = (screen_height - height) // 4

    Window.size = (width, height)
    Window.top = y
    Window.left = x
