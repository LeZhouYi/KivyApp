from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout

from core.widget.manage.style_manage import Default_Style


class ColorBoxLayout(BoxLayout):
    """自定义颜色背景布局"""
    canvas_color = ColorProperty(Default_Style["test_color"])

    def set_color(self, canvas_color):
        self.canvas_color = canvas_color


class MainBoxLayout(ColorBoxLayout):
    """主题背景布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_color(Default_Style["main_color"])


class PartBoxLayout(ColorBoxLayout):
    """次级主题背景布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_color(Default_Style["part_color"])
