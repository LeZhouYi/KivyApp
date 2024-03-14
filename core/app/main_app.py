from kivy.app import App
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from core.app.app_control import AppController
from core.app.skin_manage_app import SkinManageApp
from core.util.kivyutil import set_center_window

Builder.load_file("src/kvs/main_app.kv")


class MainLayout(BoxLayout):
    """主界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SidebarPopup(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(App, AppController):
    """主程序入口"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skin_manage_app = SkinManageApp()

    def build(self):
        self.title = "Little App"
        set_center_window(1000, 600)
        self.cache_widget(MainLayout(), "mainLayout")
        self.cache_widget(SidebarPopup(), "sidebarPopup")
        self.__bind_events()
        return self.get_widget("mainLayout")

    def on_start(self):
        skin_content_widget = self.skin_manage_app.get_widget("skinManageLayout")
        self.get_widget("main_content_layout").add_widget(skin_content_widget)

    def __bind_events(self):
        """绑定所有控件的事件"""
        self.skin_manage_app.bind_event("skin_menu", on_press=self.display_sidebar)

    def display_sidebar(self, widget: Widget):
        """显示侧边栏"""
        self.get_widget("sidebarPopup").open()
