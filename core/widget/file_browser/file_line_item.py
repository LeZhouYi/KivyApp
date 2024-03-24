from kivy.properties import StringProperty, ColorProperty
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from core.widget.base.boxlayout import LineBoxLayout
from core.widget.style_manage import Default_Style
from core.widget.base.label import BottomLineLabel
from core.widget.widget_manage import WidgetManager


class FileLineItem(LineBoxLayout, WidgetManager):
    icon_source = StringProperty(Default_Style["icon_source"])
    hover_color = ColorProperty(Default_Style["hover_color"])

    def __init__(self, file_type: str, text: str, **kwargs):
        super().__init__(**kwargs)
        self.file_type = file_type
        self.text = text
        self.is_selected = False
        self.__config()

    def __config(self):
        if self.file_type == "folder":
            self.icon_source = "src/textures/icon/folder_icon.png"
        self.ids["file_item_icon"].set_icon(self.icon_source)
        self.ids["file_item_text"].text = self.text
        self.ids["file_item_text"].bind_event("on_tap", self.on_tap)

    def on_tap(self, event):
        """点击Label事件"""
        self.is_selected = not self.is_selected
        if self.is_selected:
            with self.canvas.before:
                Color(*self.hover_color[:-1])
                Rectangle(pos=self.pos, size=(self.width, dp(2)))
            self.add_confirm_button()
        else:
            with self.canvas.before:
                Color(*self.part_color[:-1])
                Rectangle(pos=self.pos, size=(self.width, dp(2)))
            self.remove_confirm_button()

    def remove_confirm_button(self):
        """移除确认按钮"""
        button = self.get_widget("confirmButton")
        self.ids["main_layout"].remove_widget(button)

    def add_confirm_button(self):
        """添加确认按钮"""
        button = self.cache_widget("confirmButton", BottomLineLabel())
        button.text = "Confirm Select"
        self.ids["main_layout"].add_widget(button)
