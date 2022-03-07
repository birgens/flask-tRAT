import uuid
import itertools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('tRAT', __name__)


@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    pass

@bp.route('/create_test', methods=('GET','POST'))
def create_test():
    db = get_db()
    author = db.execute('SELECT id FROM user').fetchone()
    test = db.execute(
        'INSERT INTO test (author_id, title, body)'
        ' VALUES (?, ?, ?)',
        (author['id'], "test", "testbody")
    )
    question = db.execute(
        'INSERT INTO question (test_id, title, prompt)'
        ' VALUES (?, ?, ?)',
        (test.lastrowid, 'qtitle', 'qbody')
    )
    answer1 = db.execute(
        'INSERT INTO answer (question_id, body, weight)'
        ' VALUES (?,?,?)',
        (question.lastrowid, "ans1", 0)
    )
    answer2 = db.execute(
        'INSERT INTO answer (question_id, body, weight)'
        ' VALUES (?,?,?)',
        (question.lastrowid, "ans2", 100)
    )
    ttuuid = str(uuid.uuid4())
    test_taker = db.execute(
        'INSERT INTO test_taker (test_id, url)'
        ' VALUES (?, ?)',
        (test.lastrowid,ttuuid)
    )
    
    
    db.commit()
    return ttuuid

@bp.route('/tRAT/<url>', methods=('GET','POST'))
def tRAT(url):
    db = get_db()
    test = db.execute('SELECT test.id, title, body'
                      ' FROM test'
                      ' INNER JOIN test_taker ON test_taker.test_id = test.id'
                      ' WHERE url = ?', (url,)).fetchone()
    # questions = db.execute('SELECT  '
    questions_answers = db.execute('SELECT q.id, q.prompt, a.id AS a_id, a.body'
                           ' FROM question q'
                           ' JOIN answer a ON q.id == a.question_id'
                           ' WHERE test_id = ?', (test['id'],)).fetchall()
    print(questions_answers)
    questions = []
    for q, a in itertools.groupby(questions_answers, key=lambda r: r[0]):
        id = q
        aa = list(a)
        prompt = aa[0]['prompt']
        questions.append({'id': id, 'prompt': prompt, 'answers': [ans for ans in aa]})
    print(questions)
        
    return render_template("tRAT/tRAT.html",test=test,questions=questions)

@bp.route('/tRAT/<url>/answer/', methods=['POST'])
def post_answer(url):
    db = get_db()
    
    taker_id = db.execute('SELECT test_taker.id'
                          ' FROM test_taker'
                          ' WHERE url = ?', (url,)).fetchone()

    answer_id = request.json['id']

    print(taker_id[0],answer_id)
    print(type(taker_id[0]),type(answer_id))
    if not request.json:
        abort(400)

    answer = db.execute('SELECT id, weight'
                        ' FROM answer'
                        ' WHERE id=?', (answer_id,)).fetchone()

    taker_answer = db.execute('INSERT INTO taker_answer (answer_id, testtaker_id)'
                              ' VALUES (?, ?)',
                              (answer_id, taker_id)
    )
    
    return({'id':id, 'weight':answer['weight']})
    if answer['weight'] == 100:
        return str('Correct')
    else:
        return str('Incorrect')

    
