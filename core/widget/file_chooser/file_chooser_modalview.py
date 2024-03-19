import re

from kivy.uix.modalview import ModalView

from core.util.data_util import *
from core.util.kivy_util import *
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

    def __init_config(self):
        self.add_folder_black_list(r"^\.[\S]*")  # 忽略带.的文件夹

    def clear_content(self):
        """清除内容"""
        self.ids["scroll_list_layout"].clear_widgets()

    def load_folder(self, folder: str = None):
        """加载当前文件夹"""
        self.now_folder = folder
        if is_empty(self.now_folder) or not os.path.exists(self.now_folder):
            self.now_folder = os.getcwd()
        self.clear_content()
        self.add_back_item()
        # 遍历并生成当前所有文件夹
        for file_name in os.listdir(self.now_folder):
            if os.path.isdir(os.path.join(self.now_folder, file_name)):
                if not self.is_folder_black_lists(file_name):
                    self.add_folder_item(file_name)
        scroll_list_layout = self.ids["scroll_list_layout"]
        scroll_list_layout.height = calculate_height(scroll_list_layout)

    def add_folder_item(self, file_name):
        """添加单个文件夹"""
        widget_key = create_key("folderItem", file_name)
        widget = self.cache_widget(FolderLineLayout(), widget_key)
        text_label = widget.ids["folder_text_label"]
        text_label.text = file_name
        text_label.bind_event("on_double_tap", event_adaptor(
            self.on_double_click_folder_item, file_name=file_name
        ))
        text_label.bind_event("on_tap", event_adaptor(
            self.on_click_folder_item, file_name=file_name
        ))
        self.ids["scroll_list_layout"].add_widget(widget)

    def add_back_item(self):
        """添加返回上一页"""
        widget_key = create_key("folderItem", "back")
        widget = self.cache_widget(FolderLineLayout(), widget_key)
        text_label = self.get_child_widget(widget_key, "folder_text_label")
        text_label.text = "..."
        text_label.bind_event("on_double_tap", self.on_double_click_back)
        self.ids["scroll_list_layout"].add_widget(widget)

    def add_folder_black_list(self, pattern: str):
        """添加文件夹黑名单"""
        self.folder_black_lists.append(pattern)

    def is_folder_black_lists(self, folder_name: str) -> bool:
        """判断当前文件夹名是否在黑名单中"""
        for pattern in self.folder_black_lists:
            if re.match(pattern, folder_name):
                return True
        return False

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
        self.run_event("on_click_confirm_button")

    def get_select_folder(self) -> str:
        """获取当前选取的folder"""
        if self.now_selected_folder is None:
            return self.now_folder
        return os.path.join(self.now_folder, self.now_selected_folder)
