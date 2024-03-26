from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout

from core.app.skin_manage.skin_setting_modalview import SkinSettingModalView
from core.app.skin_manage.skin_item_layout import SkinItemLayout
from core.data.skin_manage_data import SkinManageData
from core.widget.base.button import IconButton  # type:ignore
from core.widget.base.gridlayout import MainGridLayout  # type: ignore
from core.widget.style_manage import Default_Style
from core.widget.widget_manage import WidgetManager


class SkinManageLayout(BoxLayout, WidgetManager, SkinManageData):
    info_font_color = ColorProperty(Default_Style["info_font_color"])
    font_color = ColorProperty(Default_Style["font_color"])

    def __init__(self):
        super().__init__()
        SkinManageData.__init__(self, file_path="data/app/skin_manage.json")
        self.__init_widget()

    def __init_widget(self):
        """控件配置"""
        setting_view = self.cache_widget("settingModalView", SkinSettingModalView())
        setting_view.bind(on_dismiss=self.on_setting_dismiss)
        self.ids["menu_button"].set_icon(Default_Style["menu_icon"], Default_Style["menu_icon_active"])
        self.ids["setting_button"].set_icon(Default_Style["setting_icon"],
                                            Default_Style["setting_icon_active"])
        self.ids["setting_button"].bind(on_release=self.on_open_setting)
        self.update_role_list()

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

    def update_role_list(self):
        """更新角色列表内容"""
        layout = self.ids["skin_grid_layout"]
        for role, value in self.roles.items():
            widget_key = self.create_key("roleItem", role)
            widget = self.cache_widget(widget_key, SkinItemLayout())
            widget.set_role_data(value)
            layout.add_widget(widget)

    def update_grid_layout(self):
        """更新网格布局的单行显示数，调整布局的高度"""

    def on_setting_dismiss(self, event):
        """设置页面关闭事件"""
        # TODO: 刷新设置变更后影响的页面内容
