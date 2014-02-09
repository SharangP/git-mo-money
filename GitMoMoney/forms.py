from flask.ext.wtf import Form
from wtforms import (TextField, IntegerField, FloatField, validators,
        SelectMultipleField, widgets)

class RepositoryForm(Form):
    repo_owner = TextField('Repository Owner:', [validators.Length(min=1, max=35)])
    repo_name = TextField('Repository Name:', [validators.Length(min=1, max=35)])

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CollaboratorsForm(Form):
    collaborators = MultiCheckboxField('Collaborators', coerce=int)

class OptionsForm(Form):
    max_money = FloatField('Max Amount of Money To Pay:')
    num_commits = IntegerField('Number Commits Threshold:')
    num_lines = IntegerField('Number Lines Threshold:')

    @classmethod
    def append_field(cls, name, field):
        setattr(cls, name, field)
        return cls
