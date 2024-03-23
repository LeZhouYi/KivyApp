def event_adaptor(method, **kwargs):
    """为控件事件实现带参数方法"""
    return lambda event, fun=method, params=kwargs: fun(event, **params)


class EventMapper:
    """提供控件事件映射的一套方法"""

    def __init__(self):
        self.event_mapper = {}

    def bind_event(self, event_key: str, func):
        """绑定事件"""
        self.event_mapper[event_key] = func

    def run_event(self, event_key: str):
        """执行事件"""
        if event_key in self.event_mapper:
            func = self.event_mapper[event_key]
            if func is not None:
                func(self)
