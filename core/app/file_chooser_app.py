from core.util.data_util import *
from core.widget.controller import Controller
from core.widget.file_chooser import FileChooserModalView


class FileChooserApp(Controller):
    """文件浏览应用"""

    def __init__(self):
        Controller.__init__(self)
        self.__init_widget()
        self.__init_config()

    # ---------------Controller初始化方法---------------
    def __init_config(self):
        self.get_cache_widget("FileChooserModalView").add_folder_black_list(r"^\.[\S]*")  # 忽略带.的文件夹

    def __init_widget(self):
        self.cache_widget(FileChooserModalView(), "FileChooserModalView")

    def load_folder(self, folder: str = None):
        """加载当前文件夹并生成对应控件，folder需绝对路径"""
        if is_empty(folder) or not os.path.exists(folder):
            folder = os.getcwd()
        self.get_cache_widget("FileChooserModalView").load_folder(folder)
