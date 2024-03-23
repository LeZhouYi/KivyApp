from core.data.app_data import AppData


class SkinManageData(AppData):
    """皮肤管理数据"""

    def __init__(self, file_path: str):
        self.skin_store_dir = None
        super().__init__(file_path=file_path)
