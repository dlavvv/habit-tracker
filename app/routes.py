from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.forms import LoginForm, SignupForm, AddHabitForm, EditHabitForm, AddListForm, AddTaskForm, EditTaskForm
from app.models import Habits, Tasks, Lists, Users


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template("app/home.html")



# HABITS
@app.route('/habits')
@login_required
def view_habits():
    all_habits = db.session.scalars(db.select(Habits).filter_by(user_id=current_user.id)).all()
    return render_template("habits/habits.html", all_habits=all_habits)

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
    return render_template('habits/addhabit.html', form=form)

@app.route('/edithabit/<int:habit_id>', methods=['GET', 'POST'])
@login_required
def edit_habit(habit_id):
    habit = Habits.query.filter_by(id=habit_id, user_id=current_user.id).first_or_404()
    form = EditHabitForm()

    if form.validate_on_submit():
        habit.name = form.name.data
        habit.completed = form.completed.data

        if habit.completed:
            habit.completion_time = datetime.now()
        else:
            habit.completion_time = None

        db.session.commit()
        flash('Habit successfully updated!')
        return redirect(url_for('view_habits'))

    if request.method == 'GET':
        form.name.data = habit.name
        form.completed.data = habit.completed

    return render_template('habits/edithabit.html', form=form)

@app.route('/deletehabit/<int:habit_id>', methods=['GET', 'POST'])
@login_required
def del_habit(habit_id):
    habit = Habits.query.filter_by(id=habit_id, user_id=current_user.id).first_or_404()
    db.session.delete(habit)
    db.session.commit()
    flash('Habit successfully deleted!')
    return redirect(url_for('view_habits'))



# LISTS
@app.route('/lists')
@login_required
def view_lists():
    all_lists = db.session.scalars(db.select(Lists).filter_by(user_id=current_user.id)).all()
    return render_template('lists/lists.html', all_lists=all_lists)

@app.route('/addlist', methods=['GET', 'POST'])
@login_required
def add_list():
    form = AddListForm()

    if form.validate_on_submit():
        new_list = Lists(
            name=form.name.data,
            user_id=current_user.id,
            last_modified=datetime.now()
        )
        db.session.add(new_list)
        db.session.commit()
        flash('List succesfully added !')
        return redirect(url_for('home'))
    return render_template('lists/addlist.html', form=form)

@app.route('/openlist/<int:list_id>', methods=['GET'])
@login_required
def open_list(list_id):
    # current_list e intreg obiectul Lista cu id-ul selectat de noi, deci contine toate informatiile acelei liste
    current_list = Lists.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()

    list_name = current_list.name
    tasks = Tasks.query.filter_by(list_id=list_id, user_id=current_user.id).all()

    return render_template('lists/openlist.html', list_name=list_name, current_list=current_list, tasks=tasks)

@app.route('/editlist/<int:list_id>', methods=['GET','POST'])
@login_required
def edit_list(list_id):
    current_list = Lists.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    form = EditHabitForm()

    # daca editam lista si apasam 'save changes' care trimite formularul
    if form.validate_on_submit():
        if current_list.name != form.name.data:
            current_list.last_modified = datetime.now()

        current_list.name = form.name.data

        db.session.commit()
        flash('List updated succesfully !')

        return redirect(url_for('view_lists'))

    form.name.data = current_list.name

    return render_template('lists/editlist.html', form=form)

@app.route('/deletelist/<int:list_id>', methods=['GET','POST'])
@login_required
def del_list(list_id):
    current_list = Lists.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    db.session.delete(current_list)
    db.session.commit()
    flash('List succesfully deleted !')
    return redirect(url_for('view_lists'))



# TASKS
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def view_tasks():
    all_tasks = db.session.scalars(db.select(Tasks).filter_by(user_id=current_user.id)).all()
    return render_template("tasks/tasks.html", all_tasks=all_tasks)

@app.route('/addtask/<int:list_id>', methods=['GET', 'POST'])
@login_required
def add_task(list_id):
    form = AddTaskForm()

    if form.validate_on_submit():
        new_task = Tasks(
            description = form.description.data,
            completed = form.completed.data,
            completion_time = None,
            list_id = list_id, # e trimis din html folosind butonul de + care apeleaza /addtask
            user_id = current_user.id
        )

        db.session.add(new_task)
        db.session.commit()
        flash('Task added succesfully !')
        return redirect(url_for('home')) # momentan home

    return render_template("tasks/addtask.html", form=form)

@app.route('/edittask/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Tasks.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = EditTaskForm()

    # daca dam submit pt a salva schimbarile
    if form.validate_on_submit():
        task.description = form.description.data
        task.completed = form.completed.data

        db.session.commit()
        flash('Task updated succesfully !')

        return redirect(url_for('home'))

    form.description.data = task.description
    form.completed.data = task.completed

    return render_template("tasks/edittask.html", form=form)



# LOGIN
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
    return render_template('app/signup.html', title='Sign up', form=form)

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
    return render_template('app/login.html', title='Log in', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))