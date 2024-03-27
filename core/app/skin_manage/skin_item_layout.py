from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ColorProperty

from core.widget.base.boxlayout import MainBoxLayout
from core.widget.event_manage import EventMapper
from core.widget.style_manage import Default_Style


class SkinItemLayout(MainBoxLayout, EventMapper):
    image_source = StringProperty(Default_Style["default_role"])
    hover_color = ColorProperty(Default_Style["part_color"])
    normal_color = ColorProperty(Default_Style["main_color"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_hover = None
        self.role_data = None
        self.absolute_position = None
        self.bind(pos=self.on_pos_change)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def set_role_data(self, role_data: dict):
        """设置角色皮肤数据"""
        self.role_data = role_data
        self.image_source = self.role_data["image_source"]
        self.ids["role_label"].text = self.role_data["text"]

    def set_color(self, normal_color=None, hover_color=None):
        """设置颜色"""
        if normal_color is not None:
            self.normal_color = normal_color
            self.canvas_color = normal_color
        if hover_color is not None:
            self.hover_color = hover_color

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
        """鼠标悬停在控件上"""
        if self.is_hover is True:
            return
        self.is_hover = True
        self.canvas_color = self.hover_color

    def on_mouse_leave(self, *args):
        """鼠标离开控件"""
        if self.is_hover is False:
            return
        self.is_hover = False
        self.canvas_color = self.normal_color
