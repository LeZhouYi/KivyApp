from kivy.app import App
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from core.wigdet.widget_control import WidgetController
from core.app.skin_manage_app import SkinManageWidget
from core.util.kivyutil import set_center_window, event_adaptor
from core.data.main_app_data import MainAppData

Builder.load_file("src/kvs/main_app.kv")


class MainLayout(BoxLayout):
    """主界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SidebarPopup(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainWidget(App, WidgetController, MainAppData):
    """主程序入口"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MainAppData.__init__(self, file_path='data/app/main_app.json')
        self.skin_manage_app = None
        self.method_mapper = {
            "skinManage": self.open_skin_manage
        }

    def build(self):
        self.title = "Little App"
        set_center_window(1000, 600)
        self.cache_widget(MainLayout(), "mainLayout")
        self.cache_widget(SidebarPopup(), "sidebarPopup")
        self.__bind_events()
        return self.get_widget("mainLayout")

    def on_start(self):
        self.open_page(self.now_page, is_first=True)

    def on_stop(self):
        self.write_data()
        if self.skin_manage_app is not None:
            self.skin_manage_app.write_data()

    def __bind_events(self):
        """绑定所有控件的事件"""
        self.bind_event("skin_manage_button", on_press=event_adaptor(self.open_page_by_sidebar, page="skinManage"))

    def display_sidebar(self, widget: Widget):
        """显示侧边栏"""
        self.get_widget("sidebarPopup").open()

    def open_page_by_sidebar(self, widget: Widget, page: str):
        """通过侧边栏打开页面"""
        self.open_page(page)
        self.get_widget("sidebarPopup").dismiss()

    def open_page(self, page: str, is_first: bool = False):
        """打开页面"""
        if self.now_page == page and not is_first:
            return
        self.now_page = page
        self.get_widget("main_content_layout").clear_widgets()
        self.method_mapper[self.now_page]()

    def open_skin_manage(self):
        """打开"""
        if self.skin_manage_app is None:
            self.skin_manage_app = SkinManageWidget()
            self.skin_manage_app.bind_event("skin_menu", on_press=self.display_sidebar)
        skin_content_widget = self.skin_manage_app.get_widget("skinManageLayout")
        self.get_widget("main_content_layout").add_widget(skin_content_widget)
