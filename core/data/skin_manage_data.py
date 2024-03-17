from core.data.app_data import AppData
from core.util.data_util import *


class SkinManageData(AppData):
    """皮肤管理的基础数据结构，用于记录操作，设置路径等信息"""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        if file_path is not None:
            self.__parsed_data(load_json_by_file(file_path))
        else:
            self.skin_store_dir = None  # 皮肤存储路径

    def get_skin_store_dir(self) -> str:
        """皮肤库路径"""
        return self.skin_store_dir

    def __parsed_data(self, data: dict):
        """解析数据"""
        self.skin_store_dir = extract_value(data, "skin_store_dir", "")

    def __packed_data(self) -> dict:
        data = {
            "skin_store_dir": self.skin_store_dir
        }
        return data

    def write_data(self):
        """将数据存入本地"""
        write_data(self.__packed_data(), self.file_path)
