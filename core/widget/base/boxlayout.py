from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ColorProperty

from core.widget.style_manage import Default_Style


class ColorBoxLayout(BoxLayout):
    canvas_color = ColorProperty(Default_Style["test_color"])


class MainBoxLayout(ColorBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["main_color"]


class PartBoxLayout(ColorBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas_color = Default_Style["part_color"]


class BorderBoxLayout(BoxLayout):
    main_color = ColorProperty(Default_Style["main_color"])
    part_color = ColorProperty(Default_Style["part_color"])


class LineBoxLayout(BoxLayout):
    main_color = ColorProperty(Default_Style["main_color"])
    part_color = ColorProperty(Default_Style["part_color"])
