from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, SignUpForm
from app import db
from app.models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@auth.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)

@auth.route('/signup', methods=['POST'])
def signup_post():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)

        #add new user to the db
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/lost-password')
def lost_password():
    return 'Lost Password'