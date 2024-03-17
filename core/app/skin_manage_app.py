from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from core.widget.controller import Controller
from core.widget.file_chooser_app import FileChooserApp
from core.data.skin_manage_data import SkinManageData


class SkinManageLayout(BoxLayout):
    """皮肤管理页面布局"""


class SkinSettingModalView(ModalView):
    """皮肤设置页面模窗"""


class SkinManageApp(Controller, SkinManageData):

    def __init__(self):
        Controller.__init__(self)
        SkinManageData.__init__(self, 'data/app/skin_manage/skin_manage.json')

        self.__init_widget()
        self.__init_widget_event()

    # ---------------Controller初始化方法---------------
    def __init_widget(self):
        self.cache_widget(SkinManageLayout(), "skinManageLayout")
        self.cache_widget(SkinSettingModalView(), "skinSettingModalView")
        self.cache_app(FileChooserApp(), "SkinFileChooserApp")

    def __init_widget_event(self):
        self.bind_child_event("skinManageLayout", "skin_setting_button",
                              on_press=self.on_click_setting)
        self.bind_child_event("skinSettingModalView", "skin_list_set_button",
                              on_press=self.on_click_skin_chooser)
        self.bind_child_event("skinSettingModalView", "skin_list_arrow_button",
                              on_press=self.on_click_skin_chooser)

    # ---------------控件事件相关---------------
    def on_click_setting(self, event):
        """打开皮肤设置模窗"""
        return self.get_cache_widget("skinSettingModalView").open()

    def on_click_skin_chooser(self, event):
        """打开皮肤库路径设置模窗"""
        file_chooser = self.get_cache_app("SkinFileChooserApp")
        file_chooser.get_cache_widget("FileChooserModalView").open()
        file_chooser.load_folder(self.skin_store_dir)
