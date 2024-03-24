from kivy.uix.modalview import ModalView
from kivy.properties import ColorProperty

from core.widget.style_manage import Default_Style


class ErrorModalView(ModalView):
    font_color = ColorProperty(Default_Style["font_color"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlay_color = Default_Style["overlay_color"]

    def set_text(self, text: str):
        """设置错误文本"""
        self.ids["warning_text_label"].text = text
