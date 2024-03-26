from kivy.uix.gridlayout import GridLayout
from kivy.properties import ColorProperty

from core.widget.style_manage import Default_Style


class ColorGridLayout(GridLayout):
    """自定义颜色背景布局"""
    canvas_color = ColorProperty(Default_Style["test_color"])


class MainGridLayout(ColorGridLayout):
    """主题背景布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["main_color"]