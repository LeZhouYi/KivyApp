import json
import os


class AppData:
    """APP数据基类"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.members = []
        self.__parsed_data(self.load_json_data())

    def __parsed_data(self, data: dict):
        """将数据解析并赋值给属性"""
        for key, value in data.items():
            setattr(self, key, value)

    def write_data(self):
        """将数据存入本地"""
        if self.file_path is None:
            raise Exception("File path: cannot empty")
        file = os.path.join(os.getcwd(), self.file_path)
        if os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.__packed_data(), f, indent=4, ensure_ascii=False)

    def __packed_data(self) -> dict:
        """打包数据成为dict"""
        data = {}
        for member in self.members:
            if hasattr(self, member):
                data[member] = getattr(self, member)
        return data

    def load_json_data(self):
        """根据相对于项目根目录加载json文件数据"""
        if self.file_path is None:
            raise Exception("File path: cannot empty")
        file = os.path.join(os.getcwd(), self.file_path)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                return json.load(f)
        else:
            raise Exception("Json file: [%s] not exist" % file)
