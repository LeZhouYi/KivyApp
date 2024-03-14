import inspect
from core.util.datautil import load_json_by_file, extract_value


class SkinManageData:
    """皮肤管理的基础数据结构，用于记录操作，设置路径等信息"""

    def __init__(self, file_path: str):
        if file_path is not None:
            self.__parsed_data(load_json_by_file(file_path))
        else:
            self.skin_store_dir = None  # 皮肤存储路径

    def __parsed_data(self, data: dict):
        """解析数据"""
        self.skin_store_dir = extract_value(data, "skin_store_dir")

    def __packed_data(self) -> dict:
        """打包数据"""
        attrs = inspect.getmembers(self, lambda a: not (
                    inspect.isroutine(a) or inspect.isgetsetdescriptor(a) or inspect.ismemberdescriptor(a)))
        attr_dict = {name: value for name, value in attrs}
        return attr_dict
