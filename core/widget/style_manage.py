import json
import os

from kivy.metrics import dp


def load_style_json(style_path: str) -> dict:
    """加载控件数据"""
    if style_path is None:
        raise Exception("File path: cannot empty")
    file = os.path.join(os.getcwd(), style_path)
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    else:
        raise Exception("Json file: [%s] not exist" % file)


def patch_style(instance, style: dict):
    """应用样式"""
    for key, value in style.items():
        if hasattr(instance, key):
            setattr(instance, key, value)


Style = load_style_json("src/config/style.json")

Default_Style = {
    "main_color": "#F3F3F3",  # 主要主题色
    "part_color": "#84DCC5",  # 次要主题色
    "test_color": "#000000",  # 用于测试的颜色
    "hover_color": "#F9A79D",  # 悬停时的颜色
    "overlay_color": "#00000039",  # 模窗背景颜色
    "background_normal": "src/textures/background/background_normal.png",  # 按钮常态时背景图
    "background_down": "src/textures/background/background_down.png",  # 按钮激活时背景图
    "font_color": "#000000",  # 默认字体颜色
    "info_font_color": "#A8A8A8",  # 提示用的字体颜色
    "icon_source": "src/textures/icon/slash_icon.png",  # 默认使用的图标
    "font": "src/font/hongmengsansscmediumziti.ttf",  # 使用的字体，不使用字体显示不了中文
    "menu_icon": "src/textures/icon/menu_icon.png",
    "menu_icon_active": "src/textures/icon/white_menu_icon.png",
    "setting_icon": "src/textures/icon/setting_icon.png",
    "setting_icon_active": "src/textures/icon/white_setting_icon.png",
    "folder_icon": "src/textures/icon/folder_icon.png",
    "arrow_right_icon": "src/textures/icon/arrow_right_icon.png",
    "arrow_right_icon_active": "src/textures/icon/white_arrow_right_icon.png",
    "confirm_icon": "src/textures/icon/confirm_icon.png",
    "confirm_icon_active": "src/textures/icon/white_confirm_icon.png",
    "window_size": [dp(600), dp(400)]
}
