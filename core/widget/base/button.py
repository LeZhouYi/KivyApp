from kivy.properties import StringProperty
from kivy.uix.button import Button

from core.widget.style_manage import Default_Style


class IconButton(Button):
    """只有Icon的按钮"""
    icon_source = StringProperty(Default_Style["icon_source"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = Default_Style["font"]
        self.normal_icon = self.icon_source
        self.hover_icon = self.icon_source
        self.background_normal = Default_Style["background_normal"]
        self.background_down = Default_Style["background_down"]

    def set_icon(self, normal_icon: str, hover_icon: str = None):
        """设置图标"""
        self.normal_icon = normal_icon
        if hover_icon is not None:
            self.hover_icon = hover_icon
        else:
            self.hover_icon = normal_icon
        self.icon_source = self.normal_icon

    def on_press(self):
        self.icon_source = self.hover_icon
        super().on_press()

    def on_release(self):
        self.icon_source = self.normal_icon
        super().on_release()
