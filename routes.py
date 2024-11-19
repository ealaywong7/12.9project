from flask import Blueprint, request, jsonify, session
import json
import os

api_bp = Blueprint('api', __name__)
DATA_PATH = "data/users.json"

# 根路径访问
@api_bp.route('/', methods=['GET'])
def home():
    return "Welcome to the API", 200

# 加载用户数据
def load_users():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    return {"users": []}

# 保存用户数据
def save_users(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# 用户登录
@api_bp.route('/login', methods=['POST'])  # 路径修改
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
@api_bp.route('/logout', methods=['POST'])  # 路径修改
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"}), 200

# 输入成绩
@api_bp.route('/input-scores', methods=['POST'])  # 路径修改
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

# 获取查询成绩
@api_bp.route('/get-scores', methods=['GET'])  # 路径修改
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
