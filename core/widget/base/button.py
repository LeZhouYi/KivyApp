from kivy.properties import StringProperty
from kivy.uix.button import Button

from core.widget.style_manage import Default_Style


class IconButton(Button):
    """只有Icon的按钮"""
    icon_source = StringProperty(Default_Style["icon_source"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = Default_Style["background_normal"]
        self.background_down = Default_Style["background_down"]

    def set_icon(self, icon_source):
        """设置图标"""
        self.icon_source = icon_source


class RightIconButton(Button):
    """图标显示在文本右侧的Icon"""
    icon_source = StringProperty("src/textures/icon/slash_icon.png")
