import re

from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from core.util.data_util import *
from core.util.kivy_util import *
from core.widget.base_widget import *  # type:ignore
from core.widget.controller import Controller


class FileChooserModalView(ModalView):
    """文件浏览模窗"""


class FolderLineLayout(BoxLayout):
    """文件夹布局"""


class FileChooserApp(Controller):
    """文件浏览应用"""

    def __init__(self):
        Controller.__init__(self)
        self.now_folder = None  # 当前文件夹
        self.now_selected_folder = None  # 当前选中的文件夹
        self.folder_black_lists = []  # 黑名单正则表达式列表
        self.__init_data()
        self.__init_widget()

    # ---------------Controller初始化方法---------------
    def __init_data(self):
        self.add_folder_black_list(r"^\.[\S]*")  # 忽略带.的文件夹

    def __init_widget(self):
        self.cache_widget(FileChooserModalView(), "FileChooserModalView")

    # ---------------控件增删改查---------------
    def create_confirm_button(self) -> Widget:
        """创建确认选择按钮"""
        button = self.cache_widget(IconTextButton(), "confirmSelectButton")
        button.text = "Confirm Select"
        return button

    def load_folder(self, folder: str = None):
        """加载当前文件夹并生成对应控件，folder需绝对路径"""
        self.now_folder = folder
        if is_empty(self.now_folder) or not os.path.exists(self.now_folder):
            self.now_folder = os.getcwd()
        self.get_child_widget("FileChooserModalView", "scroll_list_layout").clear_widgets()
        self.clear_cache_widget("folderItem", True)
        self.add_back_item()
        # 遍历并生成当前所有文件夹
        for file_name in os.listdir(self.now_folder):
            if os.path.isdir(os.path.join(self.now_folder, file_name)):
                if not self.is_folder_black_lists(file_name):
                    widget = self.create_folder_item(file_name)
                    self.add_scroll_line_item(widget)

    def add_back_item(self):
        """添加返回上一页"""
        widget_key = create_key("folderItem", "back")
        widget = self.cache_widget(FolderLineLayout(), widget_key)
        text_label = self.get_child_widget(widget_key, "folder_text_label")
        text_label.text = "..."
        text_label.bind_event("on_double_tap", self.on_double_click_back)
        self.add_scroll_line_item(widget)

    def add_scroll_line_item(self, widget: Widget):
        """添加子控件，并更新滚动布局的高度"""
        scroll_list_layout = self.get_child_widget("FileChooserModalView", "scroll_list_layout")
        scroll_list_layout.add_widget(widget)
        scroll_list_layout.height = calculate_height(scroll_list_layout)

    def create_folder_item(self, file_name: str) -> Widget:
        """创建单个文件夹"""
        widget_key = create_key("folderItem", file_name)
        widget = self.cache_widget(FolderLineLayout(), widget_key)
        text_label = self.get_child_widget(widget_key, "folder_text_label")
        text_label.text = file_name
        text_label.bind_event("on_double_tap", event_adaptor(
            self.on_double_click_folder_item, file_name=file_name
        ))
        text_label.bind_event("on_tap", event_adaptor(
            self.on_click_folder_item, file_name=file_name
        ))
        return widget

    # ---------------控件事件相关---------------
    def on_double_click_back(self, event):
        """双击返回上一页"""
        parent_dir = os.path.dirname(self.now_folder)
        self.load_folder(parent_dir)

    def on_click_folder_item(self, event, file_name: str):
        """单击文件夹，显示选中效果"""
        # 清除原选择
        widget_key = create_key("folderItem", self.now_selected_folder)
        if self.exist_cache_widget(widget_key):
            widget = self.get_child_widget(widget_key, "green_line_layout")
            with widget.canvas.before:
                Color(153 / 255.0, 195 / 255.0, 159 / 255.0, 1)
                Rectangle(pos=widget.pos, size=(widget.width, dp(2)))
        # 渲染新选择
        widget_key = create_key("folderItem", file_name)
        if self.exist_cache_widget(widget_key):
            self.now_selected_folder = file_name
            widget = self.get_child_widget(widget_key, "green_line_layout")
            with widget.canvas.before:
                Color(223 / 255.0, 183 / 255.0, 161 / 255.0, 1)
                Rectangle(pos=widget.pos, size=(widget.width, dp(2)))
            content_layout = self.get_child_widget(widget_key, "line_content_layout")
            content_layout.add_widget(self.create_confirm_button())

    def on_double_click_folder_item(self, event, file_name: str):
        """双击文件夹事件，打开该文件夹"""
        self.load_folder(os.path.join(self.now_folder, file_name))

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
