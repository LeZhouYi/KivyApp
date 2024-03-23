from kivy.uix.scrollview import ScrollView
from kivy.properties import ColorProperty

from core.widget.style_manage import Default_Style


class ColorScrollView(ScrollView):
    canvas_color = ColorProperty(Default_Style["test_color"])


class MainScrollView(ColorScrollView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["main_color"]


class PartScrollView(ColorScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["part_color"]