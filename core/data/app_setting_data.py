from core.data.app_data import AppData


class AppSettingData(AppData):
    """主程序数据记录"""

    def __init__(self, file_path: str):
        self.window_size = [1000, 600]
        self.now_page = "skinManage"
        super().__init__(file_path)
