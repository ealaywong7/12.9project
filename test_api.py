import unittest
from app import create_app, db
from app.models import Judge, Team, Score, Settings

class APITestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_input_scores(self):
        # 测试输入成绩的接口
        data = {
            "judgeScores": [
                { "judgeId": 1, "scores": [80, 85, 90] },
                { "judgeId": 2, "scores": [75, 78, 88] }
            ]
        }
        response = self.client.post('/api/input-scores', json=data)
        self.assertEqual(response.status_code, 200)

    def test_query_scores(self):
        # 测试查询成绩的接口
        response = self.client.get('/api/query-scores')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
