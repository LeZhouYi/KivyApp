class AbstractData:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def __parsed_data(self, data: dict):
        """将数据解析并赋值给属性"""
        pass

    def write_data(self):
        """将数据存入本地"""
        pass

    def __packed_data(self) -> dict:
        """打包数据成为dict"""
        pass
