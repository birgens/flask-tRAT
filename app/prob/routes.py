from flask import render_template, redirect, url_for, flash, request
from app import db
from app.prob import bp
from app.models import User, TestTaker, Test, Question, Answer, AnswerTaker

@bp.route('/<taker_url>', methods=['GET', 'POST'])
def index(taker_url):
    print(TestTaker.query.all()[0])
    print(taker_url)
    test_taker = TestTaker.query.filter_by(url=taker_url).first_or_404()
    test = test_taker.test

#    print(Test.query.all())
 #   test = Test.query.filter_by(id=test_taker.test_id).first()
    print(test_taker)
    print(test)
    return render_template('prob/index.html', test=test)

@bp.route('/<taker_url>/answer', methods=['POST'])
def answer(taker_url):
    data = request.get_json() or {}
    answer = Answer.query.filter_by(id=data['id']).first()
    test_taker = TestTaker.query.filter_by(url=taker_url).first()
    answer_taker = AnswerTaker(answer=answer, test_taker=test_taker)
    test_taker.answers.append(answer_taker)
    db.session.commit()
    return {'weight': answer.weight}

    

@bp.route('/setup/<url>')
def setup(url):
    print(User.query.all()[0])
    test = Test(body="tbody", title="ttitle", author_id = User.query.all()[0].id)
    question = Question(title='qtitle', body='qbody', test=test)
    answer1 = Answer(body='a1body \(x^a\)', weight=100, question=question)
    answer2 = Answer(body='a2body', weight=0, question=question)
    test_taker = TestTaker(url=url, test=test)
    db.session.add(test)
    db.session.add(test_taker)
    db.session.commit()
    return test_taker.url

@bp.route('/overview')
def overview():
    test = Test.query.all()[1]
    print(test.to_dict())
    return render_template("prob/overview.html", test=test.to_dict())
