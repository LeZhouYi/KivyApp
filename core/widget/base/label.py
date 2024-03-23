from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import RoundedRectangle, Rectangle, Color
from kivy.metrics import dp
from kivy.properties import ColorProperty, BooleanProperty, StringProperty
from kivy.uix.label import Label

from core.widget.event_manage import EventMapper
from core.widget.style_manage import Default_Style


class IconLabel(Label):
    icon_source = StringProperty(Default_Style["icon_source"])

    def set_icon(self, icon_source: str):
        """设置图标"""
        self.icon_source = icon_source


class BottomLineLabel(Label, EventMapper):
    part_color = ColorProperty(Default_Style["part_color"])
    hover_color = ColorProperty(Default_Style["hover_color"])
    main_color = ColorProperty(Default_Style["main_color"])
    is_hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.offset = [0, 0]
        Window.bind(mouse_pos=self.on_mouse_pos)

    def set_offset(self, x, y):
        """偏移窗，如在模窗会存在位置偏，则需要传入其对应的size_hint"""
        self.offset = [(1 - x) / 2.0, (1 - y) / 2.0]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.run_event('on_tap')

    def on_mouse_pos(self, *args):
        """监听鼠标移动"""
        if not self.get_root_window():
            return
        window_size = args[0].size
        pos = args[1]
        x = pos[0] - window_size[0] * self.offset[0]
        y = window_size[1] * (1 - self.offset[1]) - pos[1]
        if self.collide_point(x, y):
            Clock.schedule_once(self.on_mouse_enter, 0)
        else:
            Clock.schedule_once(self.on_mouse_leave, 0)

    def on_mouse_enter(self, *args):
        if self.is_hover is True:
            return
        self.is_hover = True
        with self.canvas.before:
            Color(*self.hover_color[:-1])
            RoundedRectangle(pos=(self.x, self.y + dp(3)), size=(self.width, self.height - dp(3)),
                             radius=(dp(5), dp(5), 0, 0))

    def on_mouse_leave(self, *args):
        if self.is_hover is False:
            return
        self.is_hover = False
        with self.canvas.before:
            Color(*self.part_color[:-1])
            Rectangle(pos=(self.x, self.y + dp(3)), size=(self.width, self.height - dp(3)))

    # def is_enter(self,):


class ClickLabel(Label, EventMapper):
    font_color = ColorProperty(Default_Style["font_color"])
    main_color = ColorProperty(Default_Style["main_color"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.run_event('on_tap')
