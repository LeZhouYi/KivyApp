from kivy.uix.widget import Widget


class AbstractApp:
    """Kivy APP的虚拟类，提供一些便于Widget对其子控件方便操作的方法"""

    def __init__(self, layout: Widget):
        self.layout = layout  # 该应用对应的控件，通常是一个布局
        self.del_pool = {}  # 用来缓存被删除的控件，以便重新显示
        self.parent_pool = {}  # 记录被删除的控制原父控件

    def get_layout(self) -> Widget:
        """返回应用对应的布局"""
        return self.layout

    def get_ids(self):
        """返回经由.kv文件生成的控件集"""
        return self.layout.ids

    def remove_widget(self, key: str):
        """移除控件并缓存"""
        widget = self.get_widget(key)
        self.del_pool[key] = widget
        self.parent_pool[key] = widget.parent
        self.layout.remove_widget(widget)

    def reload_widget(self, key: str, index: int):
        """重新加载控件"""
        if key not in self.parent_pool:
            raise Exception("Widget Key: [%s] not found in parent_pool" % key)
        if key not in self.del_pool:
            raise Exception("Widget Key: [%s] not found in del_pool" % key)
        parent = self.parent_pool.pop(key)
        del_widget = self.del_pool.pop(key)
        parent.add_widget(del_widget, index=index)

    def get_widget(self, key: str) -> Widget:
        """获取控件"""
        if key not in self.layout.ids:
            raise Exception("Widget Key: [%s] not found in ids" % key)
        return self.layout.ids[key]

    def bind_event(self, key: str, **kwargs):
        """绑定事件"""
        self.get_widget(key).bind(**kwargs)

    def unbind_event(self, key: str, **kwargs):
        """解绑事件"""
        self.get_widget(key).unbind(**kwargs)
