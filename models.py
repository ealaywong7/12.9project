from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Judge(db.Model):
    __tablename__ = 'judges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Judge {self.name}>"

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"<Team {self.name}>"

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    judge_id = db.Column(db.Integer, db.ForeignKey('judges.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    judge = db.relationship('Judge', back_populates='scores')
    team = db.relationship('Team', back_populates='scores')

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    num_judges = db.Column(db.Integer, nullable=False)
    num_teams = db.Column(db.Integer, nullable=False)
    track = db.Column(db.String(50), nullable=False)
    scoring = db.Column(db.Integer, nullable=False)
    display_ratio = db.Column(db.Integer, nullable=False)
