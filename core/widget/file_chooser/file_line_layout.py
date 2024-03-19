from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from core.widget.base import IconTextButton, DoubleClickLabel  # type: ignore
from core.widget.controller import Controller


class FolderLineLayout(BoxLayout, Controller):
    """文件夹布局"""

    def __init__(self):
        super().__init__()
        Controller.__init__(self)

    # ------------------控件事件---------------------
    def on_selected(self, **kwargs):
        """被选中，渲染选中效果"""
        with self.ids["green_line_layout"].canvas.before:
            Color(223 / 255.0, 183 / 255.0, 161 / 255.0, 1)
            Rectangle(pos=self.pos, size=(self.width, dp(2)))
        self.add_confirm_button()
        self.get_cache_widget("confirmSelectButton").bind(**kwargs)

    def on_remove_selected(self):
        """移除选中，恢复初始状态"""
        with self.ids["green_line_layout"].canvas.before:
            Color(153 / 255.0, 195 / 255.0, 159 / 255.0, 1)
            Rectangle(pos=self.pos, size=(self.width, dp(2)))
        if self.exist_cache_widget("confirmSelectButton"):
            button = self.get_cache_widget("confirmSelectButton")
            self.ids["line_content_layout"].remove_widget(button)
        self.clear_cache_widget("confirmSelectButton", is_pattern=False)

    # ------------------控件增删改查---------------------
    def add_confirm_button(self):
        """添加确认按钮"""
        content_layout = self.ids["line_content_layout"]
        button = self.cache_widget(IconTextButton(), "confirmSelectButton")
        button.config("Confirm Select", 'src/textures/confirm_icon.png')
        content_layout.add_widget(button)

    def set_text(self, text: str):
        """设置展示文本"""
        self.ids["folder_text_label"].text = text

    def bind_event(self, key, func):
        self.ids["folder_text_label"].bind_event(key, func)
