from kivy.uix.widget import Widget


class WidgetManager:
    """提供一套实例APP管理控件、多层级控件调用/事件绑定等方法"""

    def __init__(self):
        self.widgets = {}

    def get_widget(self, key: str) -> Widget:
        if key in self.widgets:
            return self.widgets[key]
        raise Exception("Widget key: [%s] not found" % key)

    def cache_widget(self, key: str, widget: Widget):
        """缓存控件"""
        self.widgets[key] = widget
        return self.widgets[key]

    def clear_widget(self, key: str):
        """清除控件"""
        if key in self.widgets:
            self.widgets.pop(key)

    def exist_widget(self, key: str) -> bool:
        """判断控件是否存在"""
        return key in self.widgets

    @staticmethod
    def create_key(self, base_key: str, *args):
        """构建控件Key"""
        for value in args:
            base_key = "%s_%s" % (base_key, str(value))
        return base_key
