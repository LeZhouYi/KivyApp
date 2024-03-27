from kivy.properties import StringProperty

from core.widget.label.hover_label import HoverLabel
from core.widget.manage.style_manage import Default_Style


class ClickIconLabel(HoverLabel):
    """图标按钮，用Label实现的"""
    icon_source = StringProperty(Default_Style["icon_source"])
    icon_normal = StringProperty(Default_Style["icon_source"])
    icon_hover = StringProperty(Default_Style["icon_source"])

    def set_icon(self, normal_icon: str = None, hover_icon: str = None):
        """设置图标"""
        if normal_icon is not None:
            self.icon_normal = normal_icon
            self.icon_source = normal_icon
        if hover_icon is not None:
            self.icon_hover = hover_icon

    def on_mouse_enter(self, *args):
        """鼠标悬停在控件上事件"""
        if self.is_hover is False:
            self.icon_source = self.icon_hover
        super().on_mouse_enter(*args)

    def on_mouse_leave(self, *args):
        """鼠标离开控件事件"""
        if self.is_hover is True:
            self.icon_source = self.icon_normal
        super().on_mouse_leave(*args)
