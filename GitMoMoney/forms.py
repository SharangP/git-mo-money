from flask.ext.wtf import Form
from wtforms import (BooleanField, TextField, PasswordField, IntegerField,
                            SelectField, validators, HiddenField)
from flask.ext.login import current_user

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=35)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.Required(),
                                            validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class ChangePassForm(Form):
    old_password = PasswordField('Password', [validators.Required()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.Required(),
                                            validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Required()])
