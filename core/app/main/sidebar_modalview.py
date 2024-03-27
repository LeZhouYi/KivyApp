import re

from kivy.uix.modalview import ModalView

from core.widget.manage.event_manage import event_adaptor
from core.widget.manage.style_manage import Default_Style
from core.widget.label import HoverLabel


class SidebarModalView(ModalView):
    """侧边栏"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlay_color = Default_Style["overlay_color"]
        self.init_widget()

    def init_widget(self):
        """初始化控件"""
        for key, value in self.ids.items():
            if isinstance(value, HoverLabel):
                value.set_font_color(Default_Style["font_color"], Default_Style["font_color_active"])
                value.set_canvas_color(Default_Style["main_color"], Default_Style["hover_color"])

    def bind_events(self, func):
        """为侧边栏的按钮绑定点击事件"""
        for key, value in self.ids.items():
            if re.match("^page_[a-zA-Z]+$", key):
                page = str(key).split("_")[-1]
                if isinstance(value, HoverLabel):
                    value.bind_event('on_tap', event_adaptor(func, page=page))
