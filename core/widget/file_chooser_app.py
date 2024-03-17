import os
import re

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from core.widget.controller import Controller
from core.util.kivy_util import *
from core.util.data_util import *


class DoubleClickLabel(Label):
    """支持双击的Label"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.touch_start_time = None  # 记录点击时间
        self.double_tap_time = 0.3  # 双击间隔
        self.double_tap_count = 0  # 点击计数
        self.double_tap_func = None  # 双击事件

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.double_tap_count == 0:
                self.touch_start_time = Clock.get_time()
                self.double_tap_count += 1
            elif self.double_tap_count == 1:
                self.double_tap_count += 1
            return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.double_tap_count == 2:
                touch_end_time = Clock.get_time()
                time_delta = touch_end_time - self.touch_start_time
                if time_delta < self.double_tap_time:
                    self.on_double_tap()
                self.double_tap_count = 0

    def on_double_tap(self):
        """双击事件"""
        if self.double_tap_func is not None:
            self.double_tap_func(self)

    def bind_double_tap_event(self, func):
        """绑定双击事件"""
        self.double_tap_func = func


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

    # ---------------控件增删改查---------------
    def load_folder(self, folder: str = None):
        """加载当前文件夹并生成对应控件，folder需绝对路径"""
        self.now_folder = folder
        if is_empty(self.now_folder) or not os.path.exists(self.now_folder):
            self.now_folder = os.getcwd()
        self.get_child_widget("FileChooserModalView", "scroll_list_layout").clear_widgets()
        self.clear_cache_widget("folderItem", True)
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
        widget_key = create_key("folderItem", file_name)
        widget = self.cache_widget(FolderLineLayout(), widget_key)
        text_label = self.get_child_widget(widget_key, "folder_text_label")
        text_label.text = file_name
        text_label.bind_double_tap_event(
            event_adaptor(self.double_click_folder_item, file_name=file_name))
        return widget

    # ---------------控件事件相关---------------
    def double_click_folder_item(self, event, file_name: str):
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
