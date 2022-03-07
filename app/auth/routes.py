from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import RegistrationForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return "login"

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return "Already logged in"
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulations {user.username}, you are now a registered user!')
        return redirect(url_for('auth.register'))
    return render_template('auth/register.html',
                           form=form)
