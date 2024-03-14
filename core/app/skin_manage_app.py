from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.lang import Builder
from core.app.app_control import AppController
from core.data.skin_manage_data import SkinManageData

Builder.load_file("src/kvs/skin_manage_app.kv")


class SkinSettingPopup(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SkinManageLayout(BoxLayout):
    """皮肤管理页面布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SkinManageApp(AppController, SkinManageData):

    def __init__(self):
        AppController.__init__(self)
        SkinManageData.__init__(self, 'data/skin_manage/skin_manage.json')
        self.cache_widget(SkinManageLayout(), "skinManageLayout")
        self.cache_widget(SkinSettingPopup(), "skinSettingPopup")

        self.__bind_events()

    def show_setting_popup(self, widget: Widget):
        """显示设置弹窗"""
        self.get_widget("skinSettingPopup").open()

    def __bind_events(self):
        """为本页面所有控件绑定事件"""
        self.bind_event("skin_settings", on_press=self.show_setting_popup)