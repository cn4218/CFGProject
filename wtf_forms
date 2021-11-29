# VERSION ONE

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class SignUp(FlaskForm):
    """SignUp Form"""
    name = StringField(
        'Your Name',
        [DataRequired()]
    )
    body = TextAreaField(
        'What ingredient are you searching for',
        [
            DataRequired(),
            Length(min=4,
                   message=('Your message is too short.'))
        ]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

# VERSION TWO
from wtforms import Form, BooleanField, StringField, validators

class Registration(Form):
    username = StringField('Username', [validators.length(min=3, max=15)])
    email = StringField('Email Address', [validators.length(min=8, max=40)])
    accept_rules = BooleanField('I accept the terms and conditions', [validators.InputRequired()])
