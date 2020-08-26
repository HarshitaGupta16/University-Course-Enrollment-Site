from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

#ValidationError will validate foms before we even start processing the data

class LoginForm(FlaskForm):  #We need FlaskForm to validate and process our form data
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=55)])
    submit = SubmitField("Register Now")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        #we check email inside the database against the email in the form and grab the first occurance only
        if user:
            raise ValidationError("Email is already in use. Pick another one.")