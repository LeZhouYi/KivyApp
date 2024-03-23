import platform

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from screeninfo import get_monitors

from core.app.main.main_layout import MainLayout
from core.data.app_setting_data import AppSettingData
from core.widget.widget_manage import WidgetManager

Builder.load_file("src/kvs/include.kv")


class MainApp(App, AppSettingData, WidgetManager):
    """主应用"""

    def __init__(self):
        super().__init__(file_path="data/app/app_setting.json")
        WidgetManager.__init__(self)
        self.set_center_window(self.window_size)

    def build(self):
        widget = self.cache_widget("mainLayout", MainLayout())
        return widget

    def on_start(self):
        self.get_widget("mainLayout").load_page()

    @staticmethod
    def set_center_window(size: list):
        """设置窗口宽高并居中"""
        divide = 2 if platform.system() != "Windows" else 3

        monitors = get_monitors()
        screen_width = monitors[0].width
        screen_height = monitors[0].height
        x = (screen_width - size[0]) // divide
        y = (screen_height - size[1]) // divide

        Window.size = (size[0], size[1])
        Window.top = y
        Window.left = x
