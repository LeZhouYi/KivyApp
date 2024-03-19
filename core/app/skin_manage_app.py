from kivy.uix.boxlayout import BoxLayout

from core.app.skin_manage import SkinSettingModalView
from core.data.skin_manage_data import SkinManageData
from core.widget.controller import Controller
from core.widget.file_chooser import FileChooserModalView


class SkinManageLayout(BoxLayout):
    """皮肤管理页面布局"""


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
        self.cache_widget(FileChooserModalView(), "SkinChooserModalView")

    def __init_widget_event(self):
        self.bind_child_event("skinManageLayout", "skin_setting_button",
                              on_press=self.on_click_setting)
        self.get_cache_widget("skinSettingModalView").bind_events(self.on_click_skin_chooser)
        self.get_cache_widget("SkinChooserModalView").bind_event(
            "on_click_confirm_button", self.on_finish_select_skin
        )

    # ---------------控件事件相关---------------
    def on_click_setting(self, event):
        """打开皮肤设置模窗"""
        modal_view = self.get_cache_widget("skinSettingModalView")
        modal_view.open()
        modal_view.update_select_skin(self.skin_store_dir)

    def on_click_skin_chooser(self, event):
        """打开皮肤库路径设置模窗"""
        file_chooser = self.get_cache_widget("SkinChooserModalView")
        file_chooser.open()
        file_chooser.load_folder(self.skin_store_dir)

    def on_finish_select_skin(self, event):
        """结束选择皮肤路径"""
        file_chooser = self.get_cache_widget("SkinChooserModalView")
        file_chooser.dismiss()
        self.skin_store_dir = file_chooser.get_select_folder()
        modal_view = self.get_cache_widget("skinSettingModalView")
        modal_view.update_select_skin(self.skin_store_dir)
