from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email

from wtforms import ValidationError
from app.user.models import User


# login User
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"class": "form-control"}) 
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField("Запомнить меня", default=True, render_kw={"class": "form-check-input"}) 
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-outline-info"}) 

# registration user
class RegistrationForm(FlaskForm): 
    username = StringField("Username", validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField("Электронная почта", validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField("Повторите Password", validators=[DataRequired(), EqualTo("password")], render_kw={"class": "form-control"}) 
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-outline-info"})

    # my validators check doble user
    def validate_username(self, username):
        double_user = User.query.filter_by(username=username.data).count()
        if double_user > 0:
            raise ValidationError("Пользователь с таким именем уже существует!")
    
    # my validators check doble email
    def validate_email(self, email):
        double_email = User.query.filter_by(email=email.data).count()
        if double_email > 0:
            raise ValidationError("Пользователь с таким email уже существует!")

