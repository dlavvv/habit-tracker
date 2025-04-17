from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.forms import LoginForm, SignupForm, AddHabitForm
from app.models import Habits, Tasks, Lists, Users


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template("home.html")


@app.route('/addhabit', methods=['GET', 'POST'])
@login_required
def add_habit():
    form = AddHabitForm() # object of type AddHabitForm (adica va fi form pt habit)

    if form.validate_on_submit():
        new_habit = Habits(
            name=form.name.data,
            completed=False,
            user_id=current_user.id
        )
        db.session.add(new_habit)
        db.session.commit()
        flash('Habit successfully added!')
        return redirect(url_for('home'))
    return render_template('addhabit.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        user_exists = Users.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.')
            return redirect(url_for('signup'))

        new_user = Users(
            name=name,
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Sign up successful.')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Sign up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password and try again.')
    return render_template('login.html', title='Log in', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))