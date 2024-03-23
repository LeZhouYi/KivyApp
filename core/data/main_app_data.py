from core.data.app_data import AppData


class MainAppData(AppData):
    """主程序数据记录"""

    def __init__(self, file_path: str):
        self.now_page = "skinManage"
        super().__init__(file_path)
