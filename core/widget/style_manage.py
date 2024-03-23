import json
import os


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
    "main_color": "#F3F3F3",
    "part_color": "#84DCC5",
    "test_color": "#000000",
    "hover_color": "#F9A79D",
    "overlay_color": "#00000039",
    "background_normal": "src/textures/background/background_normal.png",
    "background_down": "src/textures/background/background_down.png",
    "font_color": "#000000",
    "info_font_color": "#A8A8A8",
    "icon_source": "src/textures/icon/slash_icon.png"
}
