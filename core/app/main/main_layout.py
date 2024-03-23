from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from core.app.skin_manage.skin_manage_layout import SkinManageLayout
from core.data.main_app_data import MainAppData
from core.widget.widget_manage import WidgetManager
from core.app.main.sidebar_modalview import SidebarModalView


class MainLayout(BoxLayout, WidgetManager, MainAppData):
    """主界面布局"""

    def __init__(self):
        self.now_page = "skinManage"
        super().__init__()
        MainAppData.__init__(self, "data/app/main_app.json")
        self.__init_widget()

    def __init_widget(self):
        """初始化控件"""
        sidebar = self.cache_widget("sidebar", SidebarModalView())
        sidebar.bind_events(self.on_switch_page)

    def set_content(self, widget: Widget):
        """设置内容页"""
        self.cache_widget(self.now_page, widget)
        self.ids["main_content_layout"].add_widget(widget)
        if hasattr(widget, "bind_event"):
            widget.bind_event("menu_button", on_release=self.on_click_menu)

    def load_page(self):
        """加载页面内容"""
        if self.now_page == "skinManage":
            self.set_content(SkinManageLayout())

    def clear_page(self):
        """清空当前页面内容"""
        self.ids["main_content_layout"].clear_widgets()
        self.clear_widget(self.now_page)

    # ---------------控件事件-----------------
    def on_click_menu(self, event):
        """点击菜单事件"""
        sidebar = self.get_widget("sidebar")
        sidebar.open()
        sidebar.pos = (0, sidebar.pos[1])

    def on_switch_page(self, event, page: str):
        """切换页面内容"""
        self.get_widget("sidebar").dismiss()
        if self.now_page == page and self.exist_widget(self.now_page):
            return
        else:
            self.clear_page()
        self.now_page = page
        self.load_page()
