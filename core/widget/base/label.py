from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import RoundedRectangle, Rectangle, Color
from kivy.metrics import dp
from kivy.properties import ColorProperty, BooleanProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from core.widget.event_manage import EventMapper
from core.widget.style_manage import Default_Style


class IconLabel(Label):
    icon_source = StringProperty(Default_Style["icon_source"])
    main_color = ColorProperty(Default_Style["main_color"])

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
            self.update_absolute_position()
        window_size = args[0].size
        pos = (args[1][0], window_size[1] - args[1][1])
        print(pos)
        if self.is_enter(pos):
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

    def update_absolute_position(self):
        pos = self.pos
        parent = self.parent
        print(self.pos)
        while parent:
            if not hasattr(parent, "pos"):
                break
            pos = (pos[0] + parent.pos[0], pos[1] + parent.pos[1])
            if isinstance(parent, ScrollView):
                break
            parent = parent.parent
        self.absolute_position = pos

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


class ClickLabel(Label, EventMapper):
    font_color = ColorProperty(Default_Style["font_color"])
    main_color = ColorProperty(Default_Style["main_color"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.run_event('on_tap')
