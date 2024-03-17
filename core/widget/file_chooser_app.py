import os
import re

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout

from core.widget.controller import Controller
from core.util.kivy_util import *


class FileChooserModalView(ModalView):
    """文件浏览模窗"""


class FolderLineLayout(BoxLayout):
    """文件夹布局"""


class FileChooserApp(Controller):
    """文件浏览应用"""

    def __init__(self):
        Controller.__init__(self)
        self.now_folder = None  # 当前文件夹
        self.folder_black_lists = []  # 黑名单正则表达式列表
        self.__init_data()
        self.__init_widget()

    # ---------------Controller初始化方法---------------
    def __init_data(self):
        self.add_folder_black_list(r"^\.[\S]*")  # 忽略带.的文件夹

    def __init_widget(self):
        self.cache_widget(FileChooserModalView(), "FileChooserModalView")
        self.load_folder(None)

    # ---------------控件增删改查---------------
    def load_folder(self, folder: str = None):
        self.now_folder = folder
        if self.now_folder is None or os.path.exists(self.now_folder):
            self.now_folder = os.getcwd()
        for file_name in os.listdir(self.now_folder):
            if os.path.isdir(os.path.join(self.now_folder, file_name)):
                if not self.is_folder_black_lists(file_name):
                    widget = self.create_folder_item(file_name)
                    self.add_scroll_line_item(widget)

    def add_scroll_line_item(self, widget: Widget):
        """添加子控件，并更新滚动布局的高度"""
        scroll_list_layout = self.get_child_widget("FileChooserModalView", "scroll_list_layout")
        scroll_list_layout.add_widget(widget)
        scroll_list_layout.height = calculate_height(scroll_list_layout)

    def create_folder_item(self, file_name: str) -> Widget:
        """创建单个文件夹"""
        widget_key = "folder_%s" % file_name
        widget = self.cache_widget(FolderLineLayout(), "folder_%s" % widget_key)
        widget.ids["folder_text_label"].text = file_name
        return widget

    # ---------------其它数据---------------
    def add_folder_black_list(self, pattern: str):
        """添加文件夹黑名单"""
        self.folder_black_lists.append(pattern)

    def is_folder_black_lists(self, folder_name: str) -> bool:
        """判断当前文件夹名是否在黑名单中"""
        for pattern in self.folder_black_lists:
            if re.match(pattern, folder_name):
                return True
        return False
