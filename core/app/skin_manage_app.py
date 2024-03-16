from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.lang import Builder
from core.wigdet.widget_control import WidgetController
from core.data.skin_manage_data import SkinManageData

Builder.load_file("src/kvs/skin_manage_app.kv")


class SkinFolderChooser(ModalView):
    """文件夹选择弹窗"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SkinSettingPopup(ModalView):
    """皮肤设置弹窗"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SkinManageLayout(BoxLayout):
    """皮肤管理页面布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SkinManageWidget(WidgetController, SkinManageData):

    def __init__(self):
        WidgetController.__init__(self)
        SkinManageData.__init__(self, 'data/app/skin_manage/skin_manage.json')
        self.cache_widget(SkinManageLayout(), "skinManageLayout")
        self.cache_widget(SkinSettingPopup(), "skinSettingPopup")
        # self.cache_widget(SkinFolderChooser(), "skinFolderChooser")

        self.__init_config()
        self.__bind_events()

    def __init_config(self):
        """初始控件配置，数据准备"""
        self.get_widget("skin_list_path_label").text = self.get_skin_store_dir()

    def show_folder_chooser(self, widget: Widget):
        """显示文件夹选择框"""
        # file_chooser_popup = self.get_widget("skinFolderChooser")
        # file_chooser = self.get_child_widget("skinFolderChooser", "skin_folder_view")
        # file_chooser.path = os.getcwd()
        # file_chooser_popup.open()

    def show_setting_popup(self, widget: Widget):
        """显示设置弹窗"""
        self.get_widget("skinSettingPopup").open()

    def __bind_events(self):
        """为本页面所有控件绑定事件"""
        self.bind_event("skin_settings", on_press=self.show_setting_popup)
        self.bind_event("skin_list_set_button", on_press=self.show_folder_chooser)
