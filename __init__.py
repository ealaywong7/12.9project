from flask import Flask, session
from .routes import api_bp  # 导入 routes.py 中定义的 Blueprint
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # 用于管理会话

    # 注册 Blueprint
    app.register_blueprint(api_bp, url_prefix='/api')  # 给 Blueprint 设置一个前缀

    return app
