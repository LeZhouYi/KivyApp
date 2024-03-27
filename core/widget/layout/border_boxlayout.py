from kivy.properties import ColorProperty

from core.widget.layout import MainBoxLayout
from core.widget.manage.style_manage import Default_Style


class BorderBoxLayout(MainBoxLayout):
    """边框布局"""
    border_color = ColorProperty(Default_Style["part_color"])

    def set_border_color(self, border_color: str):
        """设置边框颜色"""
        self.border_color = border_color
