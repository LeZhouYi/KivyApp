import os
import json
import inspect


def is_empty(value: str) -> None:
    """判断字符串是否为空"""
    return value is None or value == ""


def extract_value(dict_data: dict, key: str, default_value=None):
    """提取字典的数据，若不存在则返回default_value"""
    if key in dict_data:
        return dict_data[key]
    return default_value


def packed_data(instance) -> dict:
    """打包数据"""
    attrs = inspect.getmembers(instance, lambda a: not (
            inspect.isroutine(a) or inspect.isgetsetdescriptor(a) or inspect.ismemberdescriptor(a)))
    attr_dict = {name: value for name, value in attrs}
    return attr_dict


def write_data(data: dict, file_path: str) -> None:
    """将当前数据写到文件"""
    file = os.path.join(os.getcwd(), file_path)
    if os.path.exists(file):
        with open(file, encoding="utf-8", mode="w") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
    else:
        raise Exception("File path: [%s] not exist" % file_path)


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
