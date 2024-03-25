from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import RoundedRectangle, Rectangle, Color
from kivy.metrics import dp
from kivy.properties import ColorProperty, BooleanProperty, StringProperty
from kivy.uix.label import Label

from core.widget.event_manage import EventMapper
from core.widget.style_manage import Default_Style


class BaseLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = Default_Style["font"]


class IconLabel(BaseLabel):
    icon_source = StringProperty(Default_Style["icon_source"])
    main_color = ColorProperty(Default_Style["main_color"])

    def set_icon(self, icon_source: str):
        """设置图标"""
        self.icon_source = icon_source


class BottomLineLabel(BaseLabel, EventMapper):
    part_color = ColorProperty(Default_Style["part_color"])  # 次要背景
    hover_color = ColorProperty(Default_Style["hover_color"])  # hover的颜色
    main_color = ColorProperty(Default_Style["main_color"])  # 主要背景颜色
    is_hover = BooleanProperty(False)

    def __init__(self, part_color: str = None, font_color: str = None, **kwargs):
        if part_color is not None:
            self.part_color = part_color
        if font_color is not None:
            self.color = font_color
        else:
            self.color = Default_Style["main_color"]
        super().__init__(**kwargs)
        self.absolute_position = None
        self.bind(pos=self.on_pos_change)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.run_event('on_tap')

    def on_mouse_pos(self, *args):
        """监听鼠标移动"""
        if not self.get_root_window():
            return
        if self.absolute_position is None:
            self.absolute_position = self.to_window(*self.pos)
        if self.is_enter(args[1]):
            Clock.schedule_once(self.on_mouse_enter, 0)
        else:
            Clock.schedule_once(self.on_mouse_leave, 0)

    def is_enter(self, pos) -> bool:
        """判断是否进入控件"""
        if self.absolute_position[0] <= pos[0] <= self.absolute_position[0] + self.size[0]:
            if self.absolute_position[1] <= pos[1] <= self.absolute_position[1] + self.size[1]:
                return True
        return False

    def on_pos_change(self, *args):
        """监听尺寸，位置变化"""
        self.absolute_position = None

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


class ClickLabel(BaseLabel, EventMapper):
    font_color = ColorProperty(Default_Style["font_color"])
    main_color = ColorProperty(Default_Style["main_color"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.touch_start_time = None  # 记录点击时间
        self.double_tap_time = 0.3  # 双击间隔
        self.double_tap_count = 0  # 点击计数

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
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
            if self.double_tap_count != 2:
                self.run_event("on_tap")
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


class RightIconLabel(BottomLineLabel):
    icon_source = StringProperty(Default_Style["icon_source"])

    def __init__(self, part_color: str = None, font_color: str = None, **kwargs):
        self.font_color = font_color
        self.normal_icon = self.icon_source
        self.hover_icon = self.icon_source
        super().__init__(part_color, font_color, **kwargs)

    def set_icon(self, normal_icon: str, hover_icon: str = None):
        """设置图标"""
        self.normal_icon = normal_icon
        if hover_icon is not None:
            self.hover_icon = hover_icon
        else:
            self.hover_icon = normal_icon
        self.icon_source = self.hover_icon if self.is_hover else self.normal_icon

    def on_mouse_enter(self, *args):
        self.color = self.main_color
        self.icon_source = self.hover_icon
        super().on_mouse_enter(*args)

    def on_mouse_leave(self, *args):
        self.color = self.font_color
        self.icon_source = self.normal_icon
        super().on_mouse_leave(*args)
