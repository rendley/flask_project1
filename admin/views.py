from flask import Blueprint
from flask import Flask
from flask import render_template
from flask_login import current_user, login_required

blueprint = Blueprint("admin",__name__, url_prefix="/admin" )


@blueprint.route("/")
@login_required # check login to access this page
def admin():
    if current_user.is_admin:  # check admin  in session/ decorator property model User
        return "Привет админ"
    else:
        return "Ты кто?" 