from core.data.app_data import AppData


class AppSettingData(AppData):
    """主程序数据记录"""

    def __init__(self, file_path: str):
        super().__init__(file_path)
