from kivy.uix.widget import Widget


class AppController:
    """为APP提供一些对控件及其子控件缓存、修改等方便操作的方法"""

    def __init__(self):
        self.cache_layouts = {}  # 缓存的控件，一般缓存用于整体操作的控件
        self.delete_layouts = {}  # 记录被删除的控件，该控件一般用重新恢复
        self.delete_parents = {}  # 记录被删除控件的父控件，用于重新恢复

    def cache_widget(self, widget: Widget, key: str):
        """缓存控件"""
        self.cache_layouts[key] = widget

    def remove_widget(self, key: str):
        """移除控件并缓存"""
        widget = self.get_widget(key)
        self.delete_layouts[key] = widget
        self.delete_parents[key] = widget.parent
        widget.parent.remove_widget(widget)

    def reload_widget(self, key: str, index: int):
        if key not in self.delete_layouts:
            raise Exception("Widget Key: [%s] not found in deleted layouts" % key)
        if key not in self.delete_parents:
            raise Exception("Widget Key: [%s] not found in deleted layouts' parent" % key)
        parent = self.delete_parents.pop(key)
        del_widget = self.delete_layouts.pop(key)
        parent.add_widget(del_widget, index=index)

    def get_widget(self, key: str) -> Widget:
        """从缓存的控件及子控件中查找并返回对应的控件"""
        if key in self.cache_layouts:
            return self.cache_layouts[key]
        for cache_layout in self.cache_layouts.values():
            if key in cache_layout.ids:
                return cache_layout.ids[key]
        raise Exception("Widget key: [%s] not in cache widgets or their child widgets")

    def bind_event(self, key: str, **kwargs):
        """绑定事件"""
        self.get_widget(key).bind(**kwargs)

    def unbind_event(self, key: str, **kwargs):
        """解绑事件"""
        self.get_widget(key).unbind(**kwargs)