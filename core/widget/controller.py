import re

from kivy.uix.widget import Widget


class Controller:
    """提供一套实例APP管理控件、多层级控件调用/事件绑定等方法"""

    def __init__(self):
        self.cache_widgets = {}  # 缓存控件
        self.cache_apps = {}  # 缓存APP
        self.delete_parents = {}  # 记录被删除的控件的父控件，用于恢复控件

    # ---------------初始化方法---------------
    def __init_data(self):
        """初始化非控件数据"""
        pass

    def __init_widget(self):
        """初始化基础控件数据"""
        pass

    def __init_app(self):
        """初始化基础APP"""
        pass

    def __init_config(self):
        """APP及控件的基础配置"""
        pass

    def __init_widget_event(self):
        """APP及控件的基础事件绑定"""
        pass

    # ---------------缓存控件相关---------------
    def exist_cache_widget(self, key: str) -> bool:
        """判断是否存在缓存控件"""
        return key in self.cache_widgets

    def cache_widget(self, widget: Widget, key: str) -> Widget:
        """缓存控件，若存在则更新，并返回控件本身"""
        self.cache_widgets[key] = widget
        return self.cache_widgets[key]

    def get_cache_widget(self, key: str) -> Widget:
        """获取缓存的控件"""
        if key in self.cache_widgets:
            return self.cache_widgets[key]
        raise Exception("Cache widget key: [%s] not found." % key)

    def get_child_widget(self, cache_key: str, key: str) -> Widget:
        """获取缓存的控件的子控件"""
        cache_widget = self.get_cache_widget(cache_key)
        if key in cache_widget.ids:
            return cache_widget.ids[key]
        raise Exception("Child widget key: [%s] not found." % key)

    def bind_child_event(self, cache_key: str, key: str, **kwargs):
        """为子控件绑定事件"""
        self.get_child_widget(cache_key, key).bind(**kwargs)

    def clear_cache_widget(self, base_key: str, is_pattern: bool = False):
        """
            清理缓存的控件
            is_pattern=False表示只清理绝对相等的控件
            is_pattern=True表示清理包含该前缀的控件,如'folderItem',将清理'^folderItem_*'
        """
        if is_pattern:
            pattern = r"^%s_[\S]+" % base_key
            match_keys = []
            for key in self.cache_widgets.keys():
                if re.match(pattern, key):
                    match_keys.append(key)
            for key in match_keys:
                self.cache_widgets.pop(key)
        else:
            if base_key in self.cache_widgets:
                self.cache_widgets.pop(base_key)

    # ---------------缓存APP相关---------------
    def cache_app(self, app, key: str):
        """缓存实例APP并返回本身"""
        self.cache_apps[key] = app
        return self.cache_apps[key]

    def get_cache_app(self, key: str):
        """返回对应的实例APP"""
        if key in self.cache_apps:
            return self.cache_apps[key]
        raise Exception("App key: [%s] not found." % key)
