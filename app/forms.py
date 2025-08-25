from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.datetime import DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
from wtforms.widgets.core import TextArea


class SignupForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=16)])
    password_conf = PasswordField('Password Confirmation', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')



# HABITS
class AddHabitForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class EditHabitForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    completed = BooleanField('Completed')
    submit = SubmitField('Save Changes')



# LISTS
class AddListForm(FlaskForm): # lista e ca un fel de new page (gen ca in Notion, un fel de popup sau zona de scris)
    name = StringField('Name', validators=[DataRequired()])
    creation_datetime = DateTimeField('Creation Dateime')
    submit = SubmitField('Add List')

class EditListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save Changes')



# TASKS
class AddTaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()]) # trb ceva text area aici? sau schimbat din html cumva?
    completed = BooleanField('Completed') # vreau sa fac sa apara ca in notes, cu checkbox langa fiecare task
    submit = SubmitField('Add Task')

class EditTaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    completed = BooleanField('Completed')
    submit = SubmitField('Save Changes')