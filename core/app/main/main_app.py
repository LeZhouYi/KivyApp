from kivy.app import App
from kivy.lang import Builder

from core.app.main.main_layout import MainLayout
from core.data.app_setting_data import AppSettingData
from core.util.widget_utls import set_center_window
from core.widget.manage.widget_manage import WidgetManager
from core.widget.manage.style_manage import Default_Style

Builder.load_file("src/kvs/include.kv")


class MainApp(App, AppSettingData, WidgetManager):
    """主应用"""

    def __init__(self):
        super().__init__(file_path="data/app/app_setting.json")
        WidgetManager.__init__(self)
        set_center_window(Default_Style["window_size"])

    def build(self):
        widget = self.cache_widget("mainLayout", MainLayout())
        return widget

    def on_start(self):
        self.get_widget("mainLayout").load_page()
