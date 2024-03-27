from kivy.properties import StringProperty, ColorProperty
from kivy.uix.label import Label

from core.widget.manage.style_manage import Default_Style


class IconLabel(Label):
    """只显示图标的标签，无点击事件"""
    icon_source = StringProperty(Default_Style["icon_source"])
    canvas_color = ColorProperty(Default_Style["main_color"])

    def set_icon(self, icon_source: str):
        """设置图标"""
        self.icon_source = icon_source
