from flask.ext.wtf import Form
from wtforms import (BooleanField, TextField, PasswordField, IntegerField,
                            SelectField, validators, HiddenField)

class RepositoryForm(Form):
    repo_owner = TextField('Repository Owner', [validators.Length(min=1, max=35)])
    repo_name = TextField('Repository Name', [validators.Length(min=1, max=35)])
