from config import Config
import unittest
from app import create_app, db
from app.models import User, Team, Test, Question, Answer


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='Alice')
        u.set_password('wonderland')
        self.assertFalse(u.check_password('quantumland'))
        self.assertTrue(u.check_password('wonderland'))

    def test_joining_team(self):
        u = User(username="Alice")
        t = Team(name="TeamName")
        db.session.add(u)
        db.session.add(t)
        db.session.commit()
        self.assertEqual(u.teams.all(), [])
        self.assertEqual(t.teammates.all(), [])

        t.add_teammate(u)
        db.session.commit()
        self.assertTrue(u.in_team(t))
        self.assertEqual(u.teams.first().name, 'TeamName')
        self.assertTrue(t.is_teammate(u))

        t.remove_teammate(u)
        db.session.commit()
        self.assertFalse(u.in_team(t))
        self.assertEqual(u.teams.count(), 0)
        self.assertEqual(t.teammates.count(), 0)


class TestModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_creation(self):
        t = Test(title='Test title', body='This is a test')
        q = Question(title='Q title', body='This is a question')
        a1 = Answer(body='Correct', weight=100)
        a2 = Answer(body='Incorrect', weight=0)
        db.session.add(t)
        db.session.add(q)
        db.session.add(a1)
        db.session.add(a2)
        db.session.commit()

        q.add_answer(a1)
        q.add_answer(a2)
        t.add_question(q)
        db.session.commit()
        
        self.assertEqual(t.questions.count(), 1)
        self.assertEqual(t.questions.first().answers.count(), 2)

    def test_add_takers(self):
        t = Test(title='title')
        u1 = User(username='Alice')
        u2 = User(username='Bob')
        t1 = Team(name='lag')

        db.session.add(t)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(t1)

        self.assertEqual(t.takers.all(), [])

        t.add_testtaker(u1)
        t.add_testtaker(u2)
        t.add_testtaker(t1)

        db.session.commit()

        self.assertEqual(t.takers.count(), 3)
        self.assertTrue(u1.taking_test(t))
        self.assertTrue(u2.taking_test(t))
        self.assertTrue(t1.taking_test(t))

        t.remove_testtaker(u2)
        t.remove_testtaker(u1)
        t.remove_testtaker(t1)
        db.session.commit()
        self.assertEqual(t.takers.count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
