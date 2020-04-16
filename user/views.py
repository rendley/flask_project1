from flask import Blueprint
from flask import render_template

from .forms import LoginForm, RegistrationForm
from flask import current_app

from flask_login import login_user, logout_user, current_user
from app.db import db
from .models import User

from flask import redirect, url_for, flash


blueprint = Blueprint("user", __name__, url_prefix="/user")

# render form authentication
@blueprint.route("/login")
def login():
    if current_user.is_authenticated: #check user if authenticated redirect index button login does not work
        return redirect(url_for("index"))
    title = "Авторизация"
    form = LoginForm()
    return render_template("user/login.html", form=form, title=title)

# authentication and authorization
@blueprint.route("/process-login", methods=["POST", "GET"])
def process_login():
    form = LoginForm() 
    if form.validate_on_submit(): # check form
        user = User.query.filter_by(username=form.username.data).first() 
        if user and user.check_password(form.password.data): # check password 
            login_user(user, remember=form.remember_me.data) # remember user session/ time options config 
            flash("Вы вошли на сайт", "success") 
            return redirect(url_for("index")) 

    flash("Неправильное имя пользователя или пароль")
    return redirect(url_for("user.login")) 

# logout
@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились!", "success")
    return redirect(url_for("index"))

# render form registration 
@blueprint.route("/registration")
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    return render_template("user/registration.html", title="Регистрация", form=form)

# registration
@blueprint.route("/process_registration", methods=["POST", "GET"])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role="user")
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        flash("Вы успешно зарегистрировались!", "success")
        db.session.commit()
        return redirect(url_for("user.login"))
    flash("Пожалуйста исправьте ошибки в форме регистрации!", "danger")
    return redirect(url_for("user.registration"))