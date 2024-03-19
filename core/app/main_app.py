from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.core.window import Window

from screeninfo import get_monitors

from core.widget.controller import Controller
from core.app.skin_manage_app import SkinManageApp
from core.data.main_app_data import MainAppData
from core.util.data_util import is_empty
from core.util.kivy_util import event_adaptor

Builder.load_file("src/kvs/include.kv")


class MainLayout(BoxLayout):
    """主界面布局"""


class SidebarModalView(ModalView):
    """侧边栏模窗"""


class MainApp(App, Controller, MainAppData):
    """主程序"""

    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)
        Controller.__init__(self)
        MainAppData.__init__(self, file_path='data/app/main_app.json')

        self.__init_data()
        self.__init_widget()
        self.__init_config()

    # ---------------Widget继承相关方法---------------
    def build(self):
        return self.get_cache_widget("mainLayout")

    # ---------------Controller初始化方法---------------
    def __init_data(self):
        self.title = "Little App"
        self.set_center_window(1000, 600)
        self.page_mapper = {}
        self.add_page_mapper("pageSkinManage", self.open_skin_manage_page)

    def __init_widget(self):
        self.cache_widget(MainLayout(), "mainLayout")
        self.cache_widget(SidebarModalView(), "sidebarModalView")

    def __init_config(self):
        self.on_click_content_page(None, "pageSkinManage", is_first=True)

    # ---------------控件事件相关---------------
    def on_click_content_page(self, event, page: str, is_first: bool = False, **kwargs):
        """打开内容页"""
        if not is_first and self.now_page == page:
            self.get_cache_widget("sidebarModalView").dismiss()
            return
        self.now_page = page
        if is_empty(self.now_page):
            self.now_page = "pageSkinManage"
        self.page_mapper[page](is_first, **kwargs)

    def on_click_sidebar_menu(self, event):
        """打开侧边栏"""
        sidebar = self.get_cache_widget("sidebarModalView")
        sidebar.open()
        sidebar.pos = (0, sidebar.pos[1])

    # ---------------控件增删改查---------------

    def open_skin_manage_page(self, is_first: bool, **kwargs):
        """设置皮肤管理页"""
        if is_first:
            app = self.cache_app(SkinManageApp(), "SkinManageApp")
            app.bind_child_event("skinManageLayout", "skin_menu_button", on_press=self.on_click_sidebar_menu)
            self.bind_child_event("sidebarModalView", "skin_manage_button",
                                  on_press=event_adaptor(self.on_click_content_page, page="pageSkinManage"))
        else:
            app = self.get_cache_app("SkinManageApp")
        content = app.get_cache_widget("skinManageLayout")
        self.get_child_widget("mainLayout", "main_content_layout").add_widget(content)

    # ---------------其它数据---------------
    def add_page_mapper(self, key: str, func):
        """添加页面方法映射"""
        self.page_mapper[key] = func

    # ---------------常规方法---------------
    @staticmethod
    def set_center_window(width: int, height: int):
        """设置窗口宽高并居中"""
        monitors = get_monitors()
        screen_width = monitors[0].width
        screen_height = monitors[0].height
        x = (screen_width - width) // 4
        y = (screen_height - height) // 4

        Window.size = (width, height)
        Window.top = y
        Window.left = x
