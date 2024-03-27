from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.properties import ColorProperty, BooleanProperty

from core.widget.label import ClickLabel
from core.widget.manage.style_manage import Default_Style


class HoverLabel(ClickLabel):
    """下划线边框Label"""
    canvas_normal_color = ColorProperty(Default_Style["main_color"])
    canvas_hover_color = ColorProperty(Default_Style["hover_color"])
    font_normal_color = ColorProperty(Default_Style["font_color"])
    font_hover_color = ColorProperty(Default_Style["font_color_active"])
    is_hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.abs_pos = None  # 缓存计算得到的绝对位置
        self.init_widget()

    def init_widget(self):
        """初始化控件"""
        self.bind(pos=self.on_widget_change)
        self.bind(size=self.on_widget_change)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def set_canvas_color(self, normal_color: str = None, hover_color: str = None):
        """设置背景颜色及激动时的背景颜色"""
        if normal_color is not None:
            self.canvas_normal_color = normal_color
            self.canvas_color = normal_color  # 在初次赋值时执行更新，省略后续手动更新
        if hover_color is not None:
            self.canvas_hover_color = hover_color

    def set_font_color(self, normal_color: str = None, hover_color: str = None):
        """设置字体常态颜色及激活时的颜色"""
        if normal_color is not None:
            self.font_normal_color = normal_color
            self.font_color = normal_color
        if hover_color is not None:
            self.font_hover_color = hover_color

    def is_enter(self, pos) -> bool:
        """判断是否进入控件"""
        if self.abs_pos[0] <= pos[0] <= self.abs_pos[0] + self.size[0]:
            if self.abs_pos[1] <= pos[1] <= self.abs_pos[1] + self.size[1]:
                return True
        return False

    def on_mouse_pos(self, *args):
        """监听鼠标移动"""
        if not self.get_root_window():
            return
        if self.abs_pos is None:
            self.abs_pos = self.to_window(*self.pos)
        if self.is_enter(args[1]):
            Clock.schedule_once(self.on_mouse_enter, 0)
        else:
            Clock.schedule_once(self.on_mouse_leave, 0)

    def on_widget_change(self, *args):
        """监听控件尺寸，位置变化事件"""
        self.abs_pos = None

    def on_mouse_enter(self, *args):
        """鼠标悬停在控件上"""
        if self.is_hover is True:
            return
        self.is_hover = True
        self.font_color = self.font_hover_color
        with self.canvas.before:
            Color(*self.canvas_hover_color[:-1])
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

    def on_mouse_leave(self, *args):
        """鼠标离开控件"""
        if self.is_hover is False:
            return
        self.is_hover = False
        self.font_color = self.font_normal_color
        with self.canvas.before:
            Color(*self.canvas_color[:-1])
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
