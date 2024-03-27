from kivy.uix.boxlayout import BoxLayout

from core.app.skin_manage.skin_setting_modalview import SkinSettingModalView
from core.data.skin_manage_data import SkinManageData
from core.widget.layout.gridlayout import MainGridLayout  # type: ignore
from core.widget.manage.style_manage import Default_Style
from core.widget.manage.widget_manage import WidgetManager
from core.app.skin_manage.skin_list_layout import SkinListLayout


class SkinManageLayout(BoxLayout, WidgetManager, SkinManageData):

    def __init__(self):
        super().__init__()
        self.now_page = "root"
        SkinManageData.__init__(self, file_path="data/app/skin_manage.json")
        self.__init_widget()

    def __init_widget(self):
        """控件配置"""
        setting_view = self.cache_widget("settingModalView", SkinSettingModalView())
        setting_view.bind(on_dismiss=self.on_setting_dismiss)
        self.ids["menu_button"].set_icon(Default_Style["menu_icon"], Default_Style["menu_icon_active"])
        self.ids["setting_button"].set_icon(Default_Style["setting_icon"],
                                            Default_Style["setting_icon_active"])
        self.ids["setting_button"].bind_event("on_tap", self.on_open_setting)
        skin_list_screen = self.cache_widget("screenSkinList", SkinListLayout())
        skin_list_screen.set_data(self)
        skin_list_screen.update_role_list()
        self.ids["skin_screen_manager"].add_widget(skin_list_screen)

    def bind_event(self, widget_key: str, event_name: str, method):
        """为子控件绑定事件"""
        if widget_key in self.ids:
            self.ids[widget_key].bind_event(event_name, method)
        else:
            raise Exception("Widget key: [%s] not found in SkinManageLayout" % widget_key)

    def on_open_setting(self, event):
        """打开设置页面"""
        setting_view = self.get_widget("settingModalView")
        setting_view.set_data(self)
        setting_view.open()

    def on_setting_dismiss(self, event):
        """设置页面关闭事件"""
        # TODO: 刷新设置变更后影响的页面内容
