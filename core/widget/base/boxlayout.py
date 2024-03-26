from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ColorProperty

from core.widget.style_manage import Default_Style


class ColorBoxLayout(BoxLayout):
    """自定义颜色背景布局"""
    canvas_color = ColorProperty(Default_Style["test_color"])


class MainBoxLayout(ColorBoxLayout):
    """主题背景布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["main_color"]


class PartBoxLayout(ColorBoxLayout):
    """次级主题背景布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["part_color"]


class BorderBoxLayout(BoxLayout):
    """边框布局"""
    line_color = ColorProperty(Default_Style["main_color"])
    canvas_color = ColorProperty(Default_Style["part_color"])


class LineBoxLayout(BoxLayout):
    """下行线边框布局"""
    canvas_color = ColorProperty(Default_Style["main_color"])
    line_color = ColorProperty(Default_Style["part_color"])

    def get_line_color(self) -> list:
        return self.line_color
