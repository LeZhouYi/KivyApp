from kivy.uix.boxlayout import BoxLayout

from core.app.skin_manage.skin_item_layout import SkinItemLayout
from core.data.skin_manage_data import SkinManageData
from core.widget.manage.widget_manage import WidgetManager


class SkinListLayout(BoxLayout, WidgetManager):
    """皮肤列表布局"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skin_data = None
        self.__init_config()

    def __init_config(self):
        self.ids["skin_grid_layout"].bind(size=self.on_grid_size_change)

    def set_data(self, data: SkinManageData):
        """设置数据引用"""
        self.skin_data = data

    def on_grid_size_change(self, source, size):
        """更新网格布局的单行显示数，调整布局的高度"""
        widget = self.ids["skin_grid_layout"]
        amount = len(widget.children)
        if amount > 1:
            cols = (size[0] - (widget.padding[0] + widget.padding[1]) + widget.spacing[0]) / (
                    widget.children[0].width + widget.spacing[0])
            if cols > 1:
                widget.cols = int(cols)

    def update_role_list(self):
        """更新角色列表内容"""
        if self.skin_data is None:
            return
        layout = self.ids["skin_grid_layout"]
        for role, value in self.skin_data.roles.items():
            widget_key = self.create_key("roleItem", role)
            widget = self.cache_widget(widget_key, SkinItemLayout())
            widget.set_role_data(value)
            widget.bind_event("on_tap", self.on_tap_role)
            layout.add_widget(widget)

    def on_tap_role(self, event):
        """点击角色事件"""
        pass
