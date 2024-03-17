from core.data.app_data import AppData
from core.util.data_util import *


class MainAppData(AppData):
    """主程序数据记录"""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        if file_path is not None:
            self.__parsed_data(load_json_by_file(file_path))
        else:
            self.now_page = None  # 皮肤存储路径

    # ---------------数据读写---------------

    def __parsed_data(self, data: dict):
        """解析数据"""
        self.now_page = extract_value(data, "now_page", "skinManage")

    def __packed_data(self) -> dict:
        data = {
            "now_page": self.now_page
        }
        return data

    def write_data(self):
        """将数据存入本地"""
        write_data(self.__packed_data(), self.file_path)
