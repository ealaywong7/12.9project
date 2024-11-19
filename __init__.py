from flask import Flask, session
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # 用于管理会话
    return app
