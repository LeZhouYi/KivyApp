from kivy.uix.modalview import ModalView

from core.widget.base import DoubleClickLabel  # type: ignore


class SkinSettingModalView(ModalView):
    """皮肤设置页面模窗"""

    def update_select_skin(self, folder_path: str):
        """更新选择的皮肤路径"""
        self.ids["skin_list_path_label"].text = folder_path

    def bind_events(self, func):
        """绑定点击事件"""
        self.ids["skin_list_set_button"].bind(on_press=func)
        self.ids["skin_list_arrow_button"].bind(on_press=func)
        self.ids["skin_list_path_label"].bind_event("on_tap", func)
