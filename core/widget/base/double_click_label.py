from kivy.clock import Clock
from kivy.uix.label import Label

from core.widget.controller import EventMapper


class DoubleClickLabel(Label, EventMapper):
    """支持双击的Label"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        EventMapper.__init__(self)
        self.touch_start_time = None  # 记录点击时间
        self.double_tap_time = 0.3  # 双击间隔
        self.double_tap_count = 0  # 点击计数

    def on_touch_down(self, touch):
        """记录点击次数和时间"""
        super().on_touch_down(touch)
        if self.collide_point(*touch.pos) and touch.button == 'left':
            if self.double_tap_count == 0:
                self.touch_start_time = Clock.get_time()
                self.double_tap_count += 1
            elif self.double_tap_count == 1:
                touch_end_time = Clock.get_time()
                time_delta = touch_end_time - self.touch_start_time
                if time_delta < self.double_tap_time:
                    self.double_tap_count += 1
                else:
                    self.touch_start_time = Clock.get_time()
            return True

    def on_touch_up(self, touch):
        """双击同样会执行一次单击事件"""
        if self.collide_point(*touch.pos) and touch.button == 'left':
            super().on_touch_up(touch)
            if self.double_tap_count == 2:
                touch_end_time = Clock.get_time()
                time_delta = touch_end_time - self.touch_start_time
                if time_delta < self.double_tap_time:
                    self.run_event("on_double_tap")
                self.double_tap_count = 0
            else:
                self.run_event("on_tap")