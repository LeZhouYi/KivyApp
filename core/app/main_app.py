from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from core.util.kivyutil import set_center_window
from core.app.skin_manage_app import SkinManageApp
from core.app.abstract_app import AbstractApp
from kivy.uix.widget import Widget


class MainLayout(BoxLayout):
    """主界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(App, AbstractApp):
    """主APP，程序的入口"""

    Builder.load_file("src/kvs/main.kv")

    def __init__(self, **kwargs):
        super().__init__(layout=MainLayout(), **kwargs)
        self.skin_manage = SkinManageApp()

    def build(self):
        self.title = "LittleApp"
        set_center_window(1000, 600)
        return self.get_layout()

    def on_start(self):
        """初次加载默认SkinManage页面"""
        self.get_widget("main_content_layout").add_widget(self.skin_manage.get_layout())
        self.skin_manage.bind_event("skin_menu", on_press=self.close_sidebar)

    def close_sidebar(self, widget: Widget):
        """关闭侧边栏"""
        self.remove_widget("sidebar_layout")
        widget.unbind(on_press=self.close_sidebar)
        widget.bind(on_press=self.display_sidebar)

    def display_sidebar(self, widget: Widget):
        """显示侧边栏"""
        self.reload_widget("sidebar_layout", 1)
        widget.unbind(on_press=self.display_sidebar)
        widget.bind(on_press=self.close_sidebar)
