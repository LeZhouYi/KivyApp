from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.lang import Builder
from core.app.abstract_app import AbstractApp
from core.data.skin_manage_data import SkinManageData


class SkinManageLayout(BoxLayout, SkinManageData):
    """皮肤管理页面布局"""

    Builder.load_file("src/kvs/skin_manage.kv")

    def __init__(self, **kwargs):
        super().__init__(file_path='data/skin_manage/skin_manage.json', **kwargs)


class SkinSettingPopup(ModalView, AbstractApp):

    def __init__(self, **kwargs):
        super().__init__(layout=self, **kwargs)


class SkinManageApp(AbstractApp):
    """皮肤管理APP，用于管理皮肤的查看/修改/复制等功能"""

    def __init__(self):
        super().__init__(SkinManageLayout())
        self.setting_popup = SkinSettingPopup()
        self.__bind_events()

    def show_setting_popup(self, widget: Widget):
        """显示设置弹窗"""
        self.setting_popup.open()

    def __bind_events(self):
        """为本页面所有控件绑定事件"""
        self.bind_event("skin_settings", on_press=self.show_setting_popup)
