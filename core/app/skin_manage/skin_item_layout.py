from kivy.properties import StringProperty

from core.widget.base.boxlayout import MainBoxLayout
from core.widget.style_manage import Default_Style


class SkinItemLayout(MainBoxLayout):
    image_source = StringProperty(Default_Style["default_role"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
