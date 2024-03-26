import re

from kivy.uix.modalview import ModalView
from kivy.properties import ColorProperty

from core.widget.base.label import BottomLineLabel
from core.widget.event_manage import event_adaptor
from core.widget.style_manage import Default_Style


class SidebarModalView(ModalView):
    """侧边栏"""

    overlay_color = ColorProperty(Default_Style["overlay_color"])

    def bind_events(self, func):
        """为侧边栏的按钮绑定点击事件"""
        for key, value in self.ids.items():
            if re.match("^page_[a-zA-Z]+$", key):
                page = str(key).split("_")[-1]
                if isinstance(value, BottomLineLabel):
                    value.bind_event('on_tap', event_adaptor(func, page=page))
                    value.set_color(font_color=Default_Style["main_color"])
