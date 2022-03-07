from flask import render_template, request
from flask_login import login_required
from app import db
from app.test import bp
from app.models import Test, Answer


@login_required
@bp.route('/iRAT/<int:test_id>', methods=['GET', 'POST'])
def iRAT(test_id):
    test = Test.query.filter_by(id=test_id).first_or_404()
    return render_template("test/test.html", test=test)


@login_required
@bp.route('/answer', methods=['POST'])
def answer():
    data = request.get_json() or {}
    print('data', data)
    answer = Answer.query.filter_by(id=data['answer_id']).first()
#    result = test.answers(data)
    db.session.commit()
    return {'weight': answer.weight}


