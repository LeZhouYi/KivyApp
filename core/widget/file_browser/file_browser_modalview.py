import os
import re
from typing import Optional

import psutil
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.modalview import ModalView

from core.widget.view.error_modalview import ErrorModalView
from core.widget.manage.event_manage import EventMapper
from core.widget.file_browser.file_line_item import FileLineItem
from core.widget.manage.style_manage import Default_Style
from core.widget.manage.widget_manage import WidgetManager


def check_folder_permission(folder: str) -> bool:
    try:
        if len(os.listdir(folder)) >= 0:
            return True
    except PermissionError:
        error_view = ErrorModalView()
        error_view.set_text("没有权限访问此文件夹")
        error_view.open()
    except FileNotFoundError:
        error_view = ErrorModalView()
        error_view.set_text("文件夹 [%s] 不存在" % folder)
        error_view.open()
    return False


def check_folder(folder: str) -> Optional[str]:
    """
        检查文件夹是否存在，不存在则默认当前项目根目录；
        检查当前文件夹是否具有访问权限，不具有则有提示弹窗并返回None
    """
    if folder is None or not os.path.exists(folder):
        folder = os.getcwd()
    if check_folder_permission(folder):
        return folder
    return None


class FileBrowserModalView(ModalView, WidgetManager, EventMapper):
    scroll_padding = NumericProperty(dp(8))
    scroll_spacing = NumericProperty(dp(8))

    folder_black_list = [r"^\.[\S]*$", r"^\$[\S]*$"]

    def __init__(self, model: str):
        super().__init__()
        EventMapper.__init__(self)
        self.display_folder = None  # 当前文件夹
        self.now_select = None  # 当前文件夹下选择的文件/文件夹
        self.size_hint = [0.8, 0.8]
        self.overlay_color = Default_Style["overlay_color"]
        self.model = model  # 当前模式，若model="folder"，则只查看/选择文件夹

    def load_folder(self, folder: str):
        """加载文件夹内容"""
        folder = check_folder(folder)
        if folder is None:
            return
        self.display_folder = folder
        self.ids["scroll_list_layout"].clear_widgets()
        self.add_folder_item("...")
        for file_name in os.listdir(self.display_folder):
            if os.path.isdir(os.path.join(self.display_folder, file_name)):
                if self.can_load_folder(file_name):
                    self.add_folder_item(file_name)
        self.update_height()

    def add_folder_item(self, folder_name: str):
        """添加单个文件夹"""
        widget = self.cache_widget(self.create_key("folder", folder_name),
                                   FileLineItem(file_type="folder", text=folder_name))
        widget.bind_event("on_tap", self.on_select_change)
        widget.bind_event("on_double_tap", self.on_open_folder)
        widget.bind_event("on_confirm_select", self.on_confirm_select)
        self.ids["scroll_list_layout"].add_widget(widget)

    def on_open_folder(self, event):
        """打开文件夹事件"""
        if event.text == "...":
            # 返回父文件夹
            parent_folder = os.path.dirname(self.display_folder)
            if parent_folder != self.display_folder:
                self.load_folder(os.path.dirname(self.display_folder))
            else:
                self.load_disks()
        else:
            self.load_folder(str(os.path.join(self.display_folder, event.text)))
        self.now_select = None

    def load_disks(self):
        """加载磁盘目录"""
        self.ids["scroll_list_layout"].clear_widgets()
        for disk in psutil.disk_partitions():
            drive_letter = disk.mountpoint
            self.add_folder_item(drive_letter)

    def on_select_change(self, event):
        """当前选择的文件夹/文件有变化"""
        if not isinstance(event, FileLineItem):
            return
        if not event.is_selected:
            self.now_select = None
        elif self.now_select is not None:
            widget_key = self.create_key("folder", self.now_select)
            widget = self.get_widget(widget_key)
            widget.remove_confirm_button()
            self.now_select = event.text
        else:
            self.now_select = event.text

    def can_load_folder(self, folder_name: str):
        """判断文件夹是否可显示"""
        for pattern in self.folder_black_list:
            if re.match(pattern, folder_name):
                return False
        return True

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

    def on_confirm_select(self, event):
        """完成文件夹/文件选择"""
        file_path = self.get_confirm_select()
        if check_folder_permission(str(file_path)):
            self.dismiss()
            self.run_event("on_confirm_select")

    def get_confirm_select(self) -> str:
        """获取当前选择的文件夹"""
        if self.now_select == "...":
            return os.path.dirname(self.display_folder)
        return str(os.path.join(self.display_folder, self.now_select))
