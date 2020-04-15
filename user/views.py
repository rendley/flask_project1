from flask import Blueprint
from flask import render_template

from .forms import LoginForm
from flask import current_app

from flask_login import login_user, logout_user, current_user
from app.db import db
from .models import User

from flask import redirect, url_for, flash


blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.route("/login")
def login():
    if current_user.is_authenticated: #check user if authenticated redirect index button login does not work
        return redirect(url_for("index"))
    title = "Авторизация"
    form = LoginForm()
    return render_template("user/login.html", form=form, title=title)


@blueprint.route("/process-login", methods=["POST", "GET"])
def process_login():
    form = LoginForm() 
    if form.validate_on_submit(): # check form
        user = User.query.filter_by(username=form.username.data).first() 
        if user and user.check_password(form.password.data): # check password 
            login_user(user, remember=form.remember_me.data) # remember user session/ time options config 
            flash("Вы вошли на сайт") 
            return redirect(url_for("index")) 

    flash("Неправильное имя пользователя или пароль")
    return redirect(url_for("user.login")) 


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились!")
    return redirect(url_for("index"))