from kivy.uix.button import Button


class IconTextButton(Button):
    """带图标文本按钮"""
    def config(self, text: str, icon: str):
        """配置文件和图标"""
        self.ids["icon_image"].source = icon
        self.text = text
