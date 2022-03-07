from datetime import datetime
from flask import current_app
from app import db,login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class TestTaker(db.Model):
    """An entity that can take/answer a test"""
    __tablename__ = "test_taker"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'test_taker',
        'polymorphic_on': type
    }

    def taking_test(self, test):
        if test in self.tests:
            return True
        else:
            return False


class User(UserMixin, TestTaker):
    """An indiviual user"""
    __tablename__ = "user"
    id = db.Column(db.Integer, db.ForeignKey("test_taker.id"), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }
    
    def __repr__(self):
        return '<User {}-{}>'.format(self.username, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def in_team(self, team):
        if team in self.teams:
            return True
        else:
            return False


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


team_user = db.Table('team_user',
                     db.Column('team_id',
                               db.Integer,
                               db.ForeignKey('team.id'),
                               primary_key=True),
                     db.Column('user_id',
                               db.Integer,
                               db.ForeignKey('user.id'),
                               primary_key=True))


class Team(TestTaker):
    __tablename__ = "team"
    id = db.Column(db.Integer, db.ForeignKey("test_taker.id"), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    teammates = db.relationship(
        'User', secondary=team_user, backref=db.backref('teams', lazy='dynamic'), lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'team'
    }

    def __repr__(self):
        return '<Team {}>'.format(self.name)

    def add_teammate(self, user):
        if user not in self.teammates:
            self.teammates.append(user)

    def remove_teammate(self, user):
        if self.is_teammate(user):
            self.teammates.remove(user)

    def is_teammate(self, user):
        if user in self.teammates:
            return True
        else:
            return False


tests_takers = db.Table('tests_takers',
                        db.Column('test_id',
                                  db.Integer,
                                  db.ForeignKey('test.id'),
                                  primary_key=True),
                        db.Column('test_taker_id',
                                  db.Integer,
                                  db.ForeignKey('test_taker.id'),
                                  primary_key=True))


class Test(db.Model):
    """Test instance, e.q. iRAT 2020-10-10"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # The users that will take the test
    takers = db.relationship('TestTaker',
                             secondary=tests_takers,
                             backref=db.backref('tests', lazy='dynamic'),
                             lazy='dynamic')
    questions = db.relationship('Question', backref='test', lazy='dynamic')
    
#    test_takers = db.relationship("AnswerTaker", backref="answer", lazy=True)

#    takers = db.relationship('TestTaker', backref='test', lazy=True)

    def __repr__(self):
        return '<Test {}, {}>'.format(self.id, self.title)

    def add_testtaker(self, testtaker):
        if testtaker not in self.takers:
            self.takers.append(testtaker)

    def remove_testtaker(self, testtaker):
        if testtaker in self.takers:
            self.takers.remove(testtaker)

    def add_question(self, question):
        if question not in self.questions:
            self.questions.append(question)

    def to_dict(self):
        return {'title': self.title,
                'id': self.id,
                'body': self.body,
                'questions': [question.to_dict() for question in self.questions]
                #                'teams': [team.to_dict(question_id) for team in self.takers]
                }


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

    def __repr__(self):
        return '<Question {}, {}>'.format(self.id, self.title)

    def add_answer(self, answer):
        self.answers.append(answer)
        

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    weight = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
#    test_takers = db.relationship("AnswerTaker", backref="answer", lazy=True)

#     takers = db.relationship('TestTaker', backref='test', lazy=True)
#     questions = db.relationship('Question', backref='test', lazy=True)

#     def __repr__(self):
#         return '<Test {}, {}>'.format(self.id, self.body)

#     def to_dict(self):
#         return {'title': self.title,
#                 'id': self.id,
#                 'body': self.body,
#                 'questions': [question.to_dict() for question in self.questions]
#                 #                'teams': [team.to_dict(question_id) for team in self.takers]
#                 }

         
# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(120))
#     body = db.Column(db.Text)
#     answers = db.relationship('Answer', backref='question', lazy=True)
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

#     def __repr__(self):
#         return '<Question {}, {}>'.format(self.id, self.title)

#     def to_dict(self):
        
#         table = AnswerTaker.query.filter_by(answertaker.answer.question==self).all()
#         print(table)
#         return("tb")

        
#         teams = TestTaker.query.filter_by(test=self.test)
#         teams_dict = []
#         for team in teams:
#             team_answers = []
#             for answer in self.answers:
#                 print(answer)
#                 print(team)
#                 print(answer.test_takers)
#                 # GJør dette heller med query for å kunne sortere!
#                # AnswerTaker.query.filter_by(test_taker_id == team.id, answer_id == answer.id)
                
#                 if team in [assoc.test_taker for assoc in answer.test_takers]:
#                     print("yes")
#                     print(team)
#                     team_answers.append({'body': answer.body,
#                                          'weight': answer.weight,
#                                          })
#                 else:
#                     print("no")
#             teams_dict.append({'id': team.id,
#                                'answers': team_answers})
#         #[teams.query
#         return {'title': self.title,
#                 'body': self.body,
#                 'teams': teams_dict#[team.to_dict(self.id) for team in teams]
#                 }

    
# class AnswerTaker(db.Model):
#     __tablename__ = 'answer_taker'
#     answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), primary_key=True)
#     test_taker_id = db.Column(db.Integer, db.ForeignKey('test_taker.id'), primary_key=True)
#     test_taker = db.relationship("TestTaker", backref="answers")
    
#     created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
# class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     weight = db.Column(db.Integer)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
#     test_takers = db.relationship("AnswerTaker", backref="answer", lazy=True)

#     def __repr__(self):
#         return "<Answer {}, {}>".format(self.id, self.body)
    
# class TestTaker(db.Model):
#     __tablename__ = "test_taker"
#     id = db.Column(db.Integer, primary_key=True)
#     url = db.Column(db.String(120),unique=True)
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
#     #answers = db.relationship("AnswerTaker",
#      #                         backref=db.backref("test_taker"))
#  #   answers = db.relationship('Answer',
#   #                            secondary=answer_taker,
#    #                           backref="test_takers")
    
#     def __repr__(self):
#         return '<TestTaker {}, {}>'.format(self.id,self.test_id)


#     def to_dict(self, question_id):
#         answers = Answer.query.filter_by(Answer.question.id == question_id)
#         return {'id': self.id,
#                 #'answers': [answers]
#                 }
