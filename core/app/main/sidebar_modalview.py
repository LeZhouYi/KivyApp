import re

from kivy.uix.modalview import ModalView

from core.widget.base.label import BottomLineLabel
from core.widget.event_manage import event_adaptor


class SidebarModalView(ModalView):
    """侧边栏"""

    def bind_events(self, func):
        """为侧边栏的按钮绑定点击事件"""
        for key, value in self.ids.items():
            if re.match("^page_[a-zA-Z]+$", key):
                page = str(key).split("_")[-1]
                if isinstance(value, BottomLineLabel):
                    value.bind_event('on_tap', event_adaptor(func, page=page))
