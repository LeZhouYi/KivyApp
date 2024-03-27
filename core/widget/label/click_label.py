from kivy.clock import Clock

from core.widget.label import ColorLabel
from core.widget.manage.event_manage import EventMapper


class ClickLabel(ColorLabel, EventMapper):
    """支持双击/单击事件Label"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap_start_time = None  # 记录点击时间
        self.tap_span_time = 0.3  # 双击间隔
        self.tap_count = 0  # 点击计数

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.tap_count == 0:
                self.tap_start_time = Clock.get_time()
                self.tap_count += 1
            elif self.tap_count == 1:
                touch_end_time = Clock.get_time()
                time_delta = touch_end_time - self.tap_start_time
                if time_delta < self.tap_span_time:
                    self.tap_count += 1
                else:
                    self.tap_start_time = Clock.get_time()
            if self.tap_count != 2:
                self.run_event("on_tap")
            return True

    def on_touch_up(self, touch):
        """双击同样会执行一次单击事件"""
        if self.collide_point(*touch.pos) and touch.button == 'left':
            super().on_touch_up(touch)
            if self.tap_count == 2:
                touch_end_time = Clock.get_time()
                time_delta = touch_end_time - self.tap_start_time
                if time_delta < self.tap_span_time:
                    self.run_event("on_double_tap")
                self.tap_count = 0
