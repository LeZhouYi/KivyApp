from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout

from core.app.skin_manage.skin_setting_modalview import SkinSettingModalView
from core.data.skin_manage_data import SkinManageData
from core.widget.base.button import IconButton  # type:ignore
from core.widget.style_manage import Default_Style
from core.widget.widget_manage import WidgetManager


class SkinManageLayout(BoxLayout, WidgetManager, SkinManageData):
    info_font_color = ColorProperty(Default_Style["info_font_color"])
    font_color = ColorProperty(Default_Style["font_color"])

    def __init__(self):
        super().__init__()
        SkinManageData.__init__(self, file_path="data/app/skin_manage.json")
        self.__config()

    def __config(self):
        """控件配置"""
        self.cache_widget("settingModalView", SkinSettingModalView())
        self.ids["menu_button"].set_icon("src/textures/icon/menu_icon.png", "src/textures/icon/white_menu_icon.png")
        self.ids["setting_button"].set_icon("src/textures/icon/setting_icon.png",
                                            "src/textures/icon/white_setting_icon.png")
        self.ids["setting_button"].bind(on_release=self.on_open_setting)

    def bind_event(self, widget_key: str, **kwargs):
        """为子控件绑定事件"""
        if widget_key in self.ids:
            self.ids[widget_key].bind(**kwargs)
        else:
            raise Exception("Widget key: [%s] not found in SkinManageLayout" % widget_key)

    def on_open_setting(self, event):
        """打开设置页面"""
        setting_view = self.get_widget("settingModalView")
        setting_view.set_data(self)
        setting_view.open()
