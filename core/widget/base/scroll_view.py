from kivy.uix.scrollview import ScrollView
from kivy.properties import ColorProperty

from core.widget.style_manage import Default_Style


class ColorScrollView(ScrollView):
    """带背景滚动区域"""
    canvas_color = ColorProperty(Default_Style["test_color"])


class MainScrollView(ColorScrollView):
    """主题色滚动区域"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["main_color"]


class PartScrollView(ColorScrollView):
    """次要主题色滚动区域"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["part_color"]