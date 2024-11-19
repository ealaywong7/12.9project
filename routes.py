from flask import Blueprint, request, jsonify, session
import json
import os

# 创建 Blueprint
api_bp = Blueprint('api', __name__)
DATA_PATH = "data/users.json"

# 加载和保存用户数据
def load_users():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    return {"users": []}

def save_users(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# 根路径访问
@api_bp.route('/', methods=['GET'])
def home():
    return "Welcome to the API", 200

# 用户登录
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    users = load_users()
    user = next((u for u in users["users"] if u["username"] == username and u["password"] == password), None)

    if user:
        session['user'] = username
        return jsonify({"message": f"Welcome, {username}!"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# 用户登出
@api_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"}), 200

# 输入成绩接口
@api_bp.route('/input-scores', methods=['POST'])
def input_scores():
    data = request.get_json()
    judge_scores = data.get('judgeScores', [])

    scores_file = "data/scores.json"
    if not os.path.exists(scores_file):
        with open(scores_file, 'w') as f:
            json.dump({"scores": []}, f)

    with open(scores_file, 'r') as f:
        scores_data = json.load(f)

    for judge_score in judge_scores:
        judge_id = judge_score['judgeId']
        scores = judge_score['scores']

        for team_id, score in enumerate(scores, start=1):
            existing_score = next(
                (s for s in scores_data["scores"] if s["judge_id"] == judge_id and s["team_id"] == team_id), None
            )
            if existing_score:
                existing_score["score"] = score
            else:
                scores_data["scores"].append({"judge_id": judge_id, "team_id": team_id, "score": score})

    with open(scores_file, 'w') as f:
        json.dump(scores_data, f, indent=4)

    return jsonify({"status": "success"}), 200

# 设置系统参数接口
@api_bp.route('/set-system-settings', methods=['POST'])
def set_system_settings():
    settings_file = "data/system_settings.json"
    data = request.get_json()

    with open(settings_file, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"status": "settings updated"}), 200

# 获取系统设置接口
@api_bp.route('/get-system-settings', methods=['GET'])
def get_system_settings():
    settings_file = "data/system_settings.json"
    if not os.path.exists(settings_file):
        return jsonify({"error": "System settings not found"}), 404

    with open(settings_file, 'r') as f:
        settings = json.load(f)

    return jsonify(settings), 200

# 获取dashboard数据接口
@api_bp.route('/get-dashboard-data', methods=['GET'])
def get_dashboard_data():
    scores_file = "data/scores.json"
    teams_file = "data/teams.json"

    if not os.path.exists(scores_file) or not os.path.exists(teams_file):
        return jsonify({"error": "Dashboard data not found"}), 404

    with open(scores_file, 'r') as f:
        scores_data = json.load(f)
    with open(teams_file, 'r') as f:
        teams = json.load(f)

    # 示例：返回团队及其平均分
    dashboard_data = []
    for team in teams:
        team_scores = [s["score"] for s in scores_data["scores"] if s["team_id"] == team["id"]]
        avg_score = sum(team_scores) / len(team_scores) if team_scores else 0
        dashboard_data.append({"team_id": team["id"], "team_name": team["name"], "average_score": avg_score})

    return jsonify({"dashboard": dashboard_data}), 200

# 获取input界面数据接口
@api_bp.route('/get-input-data', methods=['GET'])
def get_input_data():
    judges_file = "data/judges.json"
    teams_file = "data/teams.json"

    judges = []
    teams = []
    if os.path.exists(judges_file):
        with open(judges_file, 'r') as f:
            judges = json.load(f)
    if os.path.exists(teams_file):
        with open(teams_file, 'r') as f:
            teams = json.load(f)

    return jsonify({
        "judges": judges,
        "teams": teams,
        "selectedJudge": 1  # 默认选择第一个评委
    }), 200

# 获取查询成绩接口
@api_bp.route('/get-scores', methods=['GET'])
def get_scores():
    scores_file = "data/scores.json"
    teams_file = "data/teams.json"

    if not os.path.exists(scores_file) or not os.path.exists(teams_file):
        return jsonify({"message": "Scores or teams not found"}), 404

    with open(scores_file, 'r') as f:
        scores_data = json.load(f)
    with open(teams_file, 'r') as f:
        teams = json.load(f)

    result = []
    for team in teams:
        team_scores = [s["score"] for s in scores_data["scores"] if s["team_id"] == team["id"]]
        result.append({
            "id": team["id"],
            "scores": team_scores
        })

    return jsonify({"teams": result}), 200
