import os

from kivy.properties import ColorProperty
from kivy.uix.modalview import ModalView

from core.data.skin_manage_data import SkinManageData
from core.widget.file_browser.file_browser_modalview import FileBrowserModalView
from core.widget.manage.style_manage import Default_Style
from core.widget.manage.widget_manage import WidgetManager


class SkinSettingModalView(ModalView, WidgetManager):
    info_font_color = ColorProperty(Default_Style["info_font_color"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = [0.8, 0.8]
        self.overlay_color = Default_Style["overlay_color"]
        self.skin_manage_data = None
        self.__init_widget()

    def __init_widget(self):
        """控件配置"""
        self.ids["skin_folder_icon_label"].set_icon(Default_Style["folder_icon"])
        self.ids["skin_folder_label"].bind_event("on_tap", self.on_open_browser)
        self.ids["skin_tip_label"].set_font_color(Default_Style["info_font_color"],
                                                  Default_Style["main_color"])
        self.ids["skin_tip_label"].set_icon(Default_Style["arrow_right_icon"],
                                            Default_Style["arrow_right_icon_active"])
        self.ids["skin_tip_label"].bind_event("on_tap", self.on_open_browser)

    def set_data(self, skin_manage_data: SkinManageData):
        """设置皮肤数据"""
        self.skin_manage_data = skin_manage_data
        if self.skin_manage_data is not None:
            self.set_skin_folder()

    def set_skin_folder(self):
        """设置皮肤库路径"""
        if hasattr(self.skin_manage_data, "skin_store_dir"):
            folder = self.skin_manage_data.skin_store_dir
            if folder is None or not os.path.exists(folder):
                folder = os.getcwd()
                self.skin_manage_data.skin_store_dir = folder
            self.ids["skin_folder_label"].text = folder

    def on_open_browser(self, event):
        """打开文件浏览器"""
        file_browser = self.cache_widget("folderBrowser", FileBrowserModalView(model="folder"))
        file_browser.open()
        file_browser.bind_event("on_confirm_select", self.on_skin_folder_select)
        file_browser.load_folder(self.skin_manage_data.skin_store_dir)

    def on_skin_folder_select(self, event):
        """选择完皮肤文件路径"""
        if isinstance(event, FileBrowserModalView):
            self.skin_manage_data.skin_store_dir = event.get_confirm_select()
            self.clear_widget("folderBrowser")
            self.ids["skin_folder_label"].text = self.skin_manage_data.skin_store_dir
