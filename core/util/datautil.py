import os
import json


def extract_value(dict_data: dict, key: str, default_value=None):
    """提取字典的数据，若不存在则返回default_value"""
    if key in dict_data:
        return dict_data[key]
    return default_value

def load_json_by_file(data_file: str):
    """根据相对于项目根目录加载json文件数据"""
    if data_file is None:
        raise Exception("File path: cannot empty")
    file = os.path.join(os.getcwd(), data_file)
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            return json.load(f)
    else:
        raise Exception("Json file: [%s] not exist" % file)
