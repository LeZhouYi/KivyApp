import os

from kivy.uix.modalview import ModalView
from kivy.properties import ListProperty
from core.data.skin_manage_data import SkinManageData


class SkinSettingModalView(ModalView):
    size_hint = ListProperty([0.8, 0.8])

    def __init__(self):
        super().__init__()
        self.__config()
        self.skin_manage_data = None

    def __config(self):
        """控件配置"""
        self.ids["skin_folder_icon_label"].set_icon("src/textures/icon/folder_icon.png")
        self.ids["skin_folder_button"].set_icon("src/textures/icon/arrow_right_icon.png")

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
