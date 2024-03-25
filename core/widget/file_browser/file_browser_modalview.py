import os
import re
from typing import Optional

from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.modalview import ModalView

from core.widget.error_modalview import ErrorModalView
from core.widget.file_browser.file_line_item import FileLineItem
from core.widget.style_manage import Default_Style
from core.widget.widget_manage import WidgetManager


class FileBrowserModalView(ModalView, WidgetManager):
    scroll_padding = NumericProperty(dp(8))
    scroll_spacing = NumericProperty(dp(8))

    folder_black_list = [r"^\.[\S]*$", r"^\$[\S]*$"]

    def __init__(self, model: str):
        super().__init__()
        self.select_folder = None  # 当前文件夹
        self.now_select = None  # 当前文件夹下选择的文件/文件夹
        self.size_hint = [0.8, 0.8]
        self.overlay_color = Default_Style["overlay_color"]
        self.model = model  # 当前模式，若model="folder"，则只查看/选择文件夹

    def load_folder(self, folder: str):
        """加载文件夹内容"""
        folder = self.check_folder(folder)
        if folder is None:
            return
        self.select_folder = folder
        self.ids["scroll_list_layout"].clear_widgets()
        self.add_folder_item("...")
        for file_name in os.listdir(self.select_folder):
            if os.path.isdir(os.path.join(self.select_folder, file_name)):
                if self.can_load_folder(file_name):
                    self.add_folder_item(file_name)
        self.update_height()

    def add_folder_item(self, folder_name: str):
        """添加单个文件夹"""
        widget = self.cache_widget(self.create_key("folder", folder_name),
                                   FileLineItem(file_type="folder", text=folder_name))
        widget.bind_event("on_tap", self.on_select_change)
        self.ids["scroll_list_layout"].add_widget(widget)

    def on_select_change(self, event):
        """当前选择的文件夹/文件有变化"""
        if self.now_select is not None:
            pass  # TODO:清理当前选择

    def can_load_folder(self, folder_name: str):
        """判断文件夹是否可显示"""
        for pattern in self.folder_black_list:
            if re.match(pattern, folder_name):
                return False
        return True

    @staticmethod
    def check_folder(folder: str) -> Optional[str]:
        """
            检查文件夹是否存在，不存在则默认当前项目根目录；
            检查当前文件夹是否具有访问权限，不具有则有提示弹窗并返回None
        """
        if folder is None or not os.path.exists(folder):
            folder = os.getcwd()
        try:
            if os.listdir(folder):
                return folder
        except PermissionError:
            error_view = ErrorModalView()
            error_view.set_text("Error")
            error_view.open()
        return None

    def update_height(self):
        """更新最小高度"""
        scroll_layout = self.ids["scroll_list_layout"]
        child_amount = len(scroll_layout.children)
        child_height_all = 0
        for child_widget in scroll_layout.children:
            child_height_all += child_widget.height
        padding_offset = self.scroll_padding * 2
        spacing_offset = 0 if child_amount <= 1 else self.scroll_spacing * (child_amount - 1)
        scroll_layout.height = child_height_all + padding_offset + spacing_offset
