from kivy.properties import StringProperty, ColorProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp

from core.widget.style_manage import Default_Style


class IconButton(Button):
    """只有Icon的按钮"""
    icon_source = StringProperty(Default_Style["icon_source"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = Default_Style["background_normal"]
        self.background_down = Default_Style["background_down"]

    def set_icon(self, icon_source: str):
        """设置图标"""
        self.icon_source = icon_source
