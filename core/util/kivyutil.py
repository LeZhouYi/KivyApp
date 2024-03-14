from kivy.core.window import Window
from screeninfo import get_monitors


def event_adaptor(method, **kwargs):
    """为控件事件实现带参数方法"""
    return lambda event, fun=method, params=kwargs: fun(event, **params)


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
