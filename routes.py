from flask import Blueprint, request, jsonify
from . import db
from .models import Judge, Team, Score, Settings

api_bp = Blueprint('api', __name__)

# 1. 输入成绩
@api_bp.route('/input-scores', methods=['POST'])
def input_scores():
    data = request.get_json()
    judge_scores = data.get('judgeScores', [])
    
    for judge_score in judge_scores:
        judge_id = judge_score['judgeId']
        scores = judge_score['scores']
        
        for team_id, score in enumerate(scores, start=1):
            existing_score = Score.query.filter_by(judge_id=judge_id, team_id=team_id).first()
            if existing_score:
                existing_score.score = score
            else:
                new_score = Score(judge_id=judge_id, team_id=team_id, score=score)
                db.session.add(new_score)

    db.session.commit()
    return jsonify({"status": "success"}), 200

# 2. 设置系统参数
@api_bp.route('/set-settings', methods=['POST'])
def set_settings():
    data = request.get_json()
    settings = Settings(
        num_judges=data['numJudges'],
        num_teams=data['numTeams'],
        track=data['track'],
        scoring=data['scoring'],
        display_ratio=data['displayRatio']
    )
    db.session.add(settings)
    db.session.commit()
    return jsonify({"status": "success"}), 200

# 3. 获取 Dashboard 数据
@api_bp.route('/get-dashboard-data', methods=['GET'])
def get_dashboard_data():
    settings = db.session.query(Settings).first()
    if settings:
        return jsonify({
            "numTeams": settings.num_teams,
            "numJudges": settings.num_judges,
            "track": settings.track
        }), 200
    else:
        return jsonify({"message": "Settings not found"}), 404

# 4. 获取 Input 界面数据
@api_bp.route('/get-input-data', methods=['GET'])
def get_input_data():
    judges = db.session.query(Judge).all()
    teams = db.session.query(Team).all()
    scores = [[] for _ in range(len(judges))]  # 每个评委的成绩数组
    return jsonify({
        "judges": [{"id": judge.id, "name": judge.name} for judge in judges],
        "teams": [{"id": team.id, "name": team.name} for team in teams],
        "scores": scores,
        "selectedJudge": 1  # 默认选择第一个评委
    }), 200

# 5. 获取查询成绩
@api_bp.route('/get-scores', methods=['GET'])
def get_scores():
    teams = db.session.query(Team).all()
    result = []
    
    for team in teams:
        scores = {}
        for judge_id in range(1, 6):  # 假设最多5个评委
            score = db.session.query(Score).filter_by(team_id=team.id, judge_id=judge_id).first()
            if score:
                scores[judge_id] = score.score
            else:
                scores[judge_id] = None  # 如果没有评分则返回 None
        result.append({
            "id": team.id,
            "scores": scores
        })
    
    return jsonify({"teams": result}), 200

# 6. 获取系统设置
@api_bp.route('/get-settings', methods=['GET'])
def get_settings():
    settings = db.session.query(Settings).first()
    if settings:
        return jsonify({
            "numJudges": settings.num_judges,
            "numTeams": settings.num_teams,
            "track": settings.track,
            "scoring": settings.scoring,
            "displayRatio": settings.display_ratio
        }), 200
    else:
        return jsonify({"message": "Settings not found"}), 404
