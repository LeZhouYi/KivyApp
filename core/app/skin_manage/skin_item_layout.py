from kivy.clock import Clock
from kivy.properties import StringProperty

from core.widget.layout import ClickBoxLayout
from core.widget.manage.style_manage import Default_Style


class SkinItemLayout(ClickBoxLayout):
    image_source = StringProperty(Default_Style["default_role"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role_data = None

    def set_role_data(self, role_data: dict):
        """设置角色皮肤数据"""
        self.role_data = role_data
        self.image_source = self.role_data["image_source"]
        self.ids["role_label"].text = self.role_data["text"]