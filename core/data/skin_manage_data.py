from core.data.app_data import AppData


class SkinManageData(AppData):
    """皮肤管理数据"""

    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)
