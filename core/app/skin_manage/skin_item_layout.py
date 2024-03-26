from kivy.properties import StringProperty

from core.widget.base.boxlayout import MainBoxLayout
from core.widget.style_manage import Default_Style


class SkinItemLayout(MainBoxLayout):
    image_source = StringProperty(Default_Style["default_role"])

    def __init__(self, **kwargs):
        self.role_data = None
        super().__init__(**kwargs)
        self.ids["role_label"].set_color(Default_Style["main_color"], Default_Style["font_color"])

    def set_role_data(self, role_data: dict):
        """设置角色皮肤数据"""
        self.role_data = role_data
        self.image_source = self.role_data["image_source"]
        self.ids["role_label"].text = self.role_data["text"]
