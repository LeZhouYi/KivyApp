from kivy.properties import ColorProperty, ListProperty
from kivy.uix.label import Label

from core.widget.manage.style_manage import Default_Style


class ColorLabel(Label):
    """基础Label，能显示中文"""

    canvas_color = ColorProperty(Default_Style["main_color"])
    font_color = ColorProperty(Default_Style["font_color"])
    radius = ListProperty(Default_Style["default_radius"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = Default_Style["font"]
