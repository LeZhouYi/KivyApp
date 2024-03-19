import os
import re

from kivy.uix.modalview import ModalView

from core.util.data_util import is_empty
from core.util.kivy_util import create_key, event_adaptor, calculate_height
from core.widget.base import WarningTextModalView
from core.widget.controller import Controller, EventMapper
from core.widget.file_chooser.file_line_layout import FolderLineLayout


class FileChooserModalView(ModalView, Controller, EventMapper):
    """文件浏览模窗"""

    def __init__(self):
        super().__init__()
        Controller.__init__(self)
        EventMapper.__init__(self)
        self.now_folder = None
        self.now_selected_folder = None  # 当前选中的文件夹
        self.folder_black_lists = []  # 黑名单
        self.__init_config()

    # ---------------Controller初始化---------------
    def __init_config(self):
        self.add_folder_black_list(r"^\.[\S]*$")  # 忽略带.的文件夹
        self.add_folder_black_list(r"^\$[\S]*$")

    # ---------------控件增删改查---------------------
    def clear_content(self):
        """清除当前显示的列表内容"""
        self.ids["scroll_list_layout"].clear_widgets()

    def load_folder(self, folder: str = None):
        """加载当前文件夹"""
        if is_empty(folder) or not os.path.exists(folder):
            folder = os.getcwd()
        if not self.check_folder_permission(folder):
            return
        self.now_folder = folder
        self.clear_content()
        self.add_back_item()
        # 遍历并生成当前所有文件夹
        for file_name in os.listdir(self.now_folder):
            if os.path.isdir(os.path.join(self.now_folder, file_name)):
                if not self.is_folder_black_lists(file_name):
                    self.add_folder_item(file_name)
        self.update_scroll_height()

    def add_folder_item(self, file_name):
        """添加单个文件夹"""
        widget_key = create_key("folderItem", file_name)
        widget = self.cache_widget(FolderLineLayout(), widget_key)
        widget.set_text(file_name)
        widget.bind_event("on_double_tap", event_adaptor(
            self.on_double_click_folder_item, file_name=file_name
        ))
        widget.bind_event("on_tap", event_adaptor(
            self.on_click_folder_item, file_name=file_name
        ))
        self.add_scroll_widget(widget)

    def add_back_item(self):
        """添加返回上一页"""
        widget_key = create_key("folderItem", "back")
        widget = self.cache_widget(FolderLineLayout(), widget_key)
        widget.set_text(self.now_folder)
        widget.bind_event("on_double_tap", self.on_double_click_back)
        self.add_scroll_widget(widget)

    def add_scroll_widget(self, widget):
        """滚动区添加控件"""
        self.ids["scroll_list_layout"].add_widget(widget)

    def update_scroll_height(self):
        """重新计算滚动区最小高度"""
        scroll_list_layout = self.ids["scroll_list_layout"]
        scroll_list_layout.height = calculate_height(scroll_list_layout)

    # ------------------控件事件---------------------
    def on_click_folder_item(self, event, file_name: str):
        """单击文件夹，显示选中效果"""
        # 清除原选择
        if file_name == self.now_selected_folder:
            return
        widget_key = create_key("folderItem", self.now_selected_folder)
        if self.exist_cache_widget(widget_key):
            line_layout = self.get_cache_widget(widget_key)
            line_layout.on_remove_selected()
        # 渲染新选择
        widget_key = create_key("folderItem", file_name)
        if self.exist_cache_widget(widget_key):
            self.now_selected_folder = file_name
            line_layout = self.get_cache_widget(widget_key)
            line_layout.on_selected(on_press=self.on_click_confirm_button)

    def on_double_click_folder_item(self, event, file_name: str):
        """双击文件夹事件，打开该文件夹"""
        self.load_folder(os.path.join(self.now_folder, file_name))

    def on_double_click_back(self, event):
        """双击返回上一页"""
        parent_dir = os.path.dirname(self.now_folder)
        self.load_folder(parent_dir)

    def on_click_confirm_button(self, event):
        """点击选择路径方法"""
        folder = self.get_select_folder()
        if not self.check_folder_permission(folder):
            return
        self.clear_content()
        self.run_event("on_click_confirm_button")

    # ------------------其它数据---------------------
    def get_select_folder(self) -> str:
        """获取当前选取的folder"""
        if self.now_selected_folder is None:
            return self.now_folder
        return str(os.path.join(self.now_folder, self.now_selected_folder))

    def is_folder_black_lists(self, folder_name: str) -> bool:
        """判断当前文件夹名是否在黑名单中"""
        for pattern in self.folder_black_lists:
            if re.match(pattern, folder_name):
                return True
        return False

    def add_folder_black_list(self, pattern: str):
        """添加文件夹黑名单"""
        self.folder_black_lists.append(pattern)

    # ------------------常规方法---------------------
    @staticmethod
    def check_folder_permission(folder: str) -> bool:
        """检查文件夹是否具有权限"""
        try:
            if os.listdir(folder):
                return True
        except PermissionError:
            warning_modal_view = WarningTextModalView()
            warning_modal_view.set_text("No permission to access the current folder")
            warning_modal_view.open()
        return False
