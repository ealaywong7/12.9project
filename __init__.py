from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# 创建数据库实例
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # 配置数据库和其他设置
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库和迁移
    db.init_app(app)
    migrate.init_app(app, db)

    # 导入并注册蓝图（API路由）
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
