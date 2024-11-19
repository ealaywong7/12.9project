import json
import os

# 文件路径
DATA_DIR = "app"
USER_FILE = os.path.join(DATA_DIR, "users.json")
SCORES_FILE = os.path.join(DATA_DIR, "scores.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# 初始化文件
def init_file(file_path, default_data):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump(default_data, file)

# 读取文件数据
def read_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# 写入文件数据
def write_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# 初始化默认数据
init_file(USER_FILE, {"users": [{"username": "judge1", "password": "12345"}]})  # 示例用户
init_file(SCORES_FILE, {"scores": []})
init_file(SETTINGS_FILE, {"settings": {}})
