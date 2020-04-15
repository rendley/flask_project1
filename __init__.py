from flask import Flask
from app import config
from flask import render_template
from app.weather import weather_by_city

from flask import current_app

from flask_login import LoginManager
from app.db import db
from app.user.models import User


from app.user.views import blueprint as user_blueprint
from app.news.views import blueprint as news_blueprint
from app.admin.views import blueprint as admin_blueprint

def create_app(): 
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(user_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(admin_blueprint)

    # when user open page, login manager get from cookies user_id and put user_id func load_user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        title = "Flask"
        content_title = "Flask Blog"
        weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
        print(weather)
        return render_template ("index.html", title=title, content_title=content_title, weather=weather)
 

  
    return app


