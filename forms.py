from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.models import User

# Allowing users to make an account and input their data in a UI interface with the use of Flask
class UserAccountForm(FlaskForm):
    username = StringField("User", validators =[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email('Enter a valid Email address.')])
    password = PasswordField("Password", validators = [DataRequired(), Length(min=8), EqualTo('retype_password')])
    retype_password = PasswordField("Retype Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Submit")

    #  code to check if the email address has already been used
    def validate_email(self, email):
        if user_info.query.filter_by(email=filter.data).first():
            raise ValidationError('Email address already exists, please try again!')

    # code to check if the username already exists
    def validate_username(self, username):
        if user_info.query.filter_by(username=username.data).first():
            raise ValidationError("This username already exists, please try again!")

# let's users login to the account that they made previously
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(message= 'Enter a valid Email address.')])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me!")
    submit = SubmitField("Login")




