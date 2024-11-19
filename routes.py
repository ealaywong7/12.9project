from flask import Blueprint, request, jsonify, session
from .storage import read_file, write_file, SCORES_FILE, SETTINGS_FILE, USER_FILE

api_bp = Blueprint("api", __name__)

# 1. 用户登录
@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = read_file(USER_FILE)["users"]
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)

    if user:
        session["username"] = username
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# 2. 用户登出
@api_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out successfully"}), 200

# 验证登录状态的装饰器
def login_required(f):
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# 3. 输入成绩
@api_bp.route("/input-scores", methods=["POST"])
@login_required
def input_scores():
    data = request.get_json()
    scores_data = read_file(SCORES_FILE)
    scores_data["scores"].extend(data["judgeScores"])
    write_file(SCORES_FILE, scores_data)
    return jsonify({"message": "Scores saved successfully"}), 200

# 4. 设置系统参数
@api_bp.route("/set-settings", methods=["POST"])
@login_required
def set_settings():
    data = request.get_json()
    write_file(SETTINGS_FILE, {"settings": data})
    return jsonify({"message": "Settings saved successfully"}), 200

# 5. 获取系统参数
@api_bp.route("/get-settings", methods=["GET"])
@login_required
def get_settings():
    settings_data = read_file(SETTINGS_FILE)
    return jsonify(settings_data["settings"]), 200

# 6. 获取成绩
@api_bp.route("/get-scores", methods=["GET"])
@login_required
def get_scores():
    scores_data = read_file(SCORES_FILE)
    return jsonify(scores_data["scores"]), 200

# 7. 获取 Dashboard 数据
@api_bp.route("/get-dashboard-data", methods=["GET"])
@login_required
def get_dashboard_data():
    settings_data = read_file(SETTINGS_FILE).get("settings", {})
    return jsonify({
        "numTeams": settings_data.get("numTeams", 0),
        "numJudges": settings_data.get("numJudges", 0),
        "track": settings_data.get("track", ""),
    }), 200

# 8. 获取 Input 界面数据
@api_bp.route("/get-input-data", methods=["GET"])
@login_required
def get_input_data():
    judges = [{"id": idx + 1, "name": f"Judge {idx + 1}"} for idx in range(5)]  # 示例数据
    teams = [{"id": idx + 1, "name": f"Team {idx + 1}"} for idx in range(10)]  # 示例数据
    scores = [[] for _ in range(len(judges))]  # 每个评委的成绩数组

    return jsonify({
        "judges": judges,
        "teams": teams,
        "scores": scores,
        "selectedJudge": 1  # 默认选择第一个评委
    }), 200
