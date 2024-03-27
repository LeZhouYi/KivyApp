from kivy.properties import ColorProperty

from core.widget.layout import MainBoxLayout
from core.widget.manage.style_manage import Default_Style


class LineBoxLayout(MainBoxLayout):
    """下行线边框布局"""
    line_color = ColorProperty(Default_Style["part_color"])

    def set_line_color(self, line_color: str):
        """设置线条颜色"""
        self.line_color = line_color

    def get_line_color(self) -> list:
        """获取线条颜色"""
        return self.line_color
