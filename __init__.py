from flask import Flask
# import app.config
from flask import render_template
from app.weather import weather_by_city
from app.news import get_data_news
from app.model import db


from flask import current_app

from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app.model import db, News


from flask import redirect, url_for, flash

from app.user.views import blueprint as user_blueprint


def create_app(): 
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(user_blueprint)

    # when user open page, login manager get from cookies user_id and put user_id func load_user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)




    @app.route('/')
    def index():
        title = "Flask"
        content_title = "Flask Blog"
        weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
        return render_template ("index.html", title=title, content_title=content_title, weather=weather)

    @app.route('/news')
    def news():
        title = "Новости"
        content_title = "Новости Python"
        news_list = get_data_news()      
        return render_template ("news.html", title=title, 
                                newslist=news_list, content_title=content_title
                                )
    
    

    @app.route("/admin/")
    @login_required # check login to access this page
    def admin():
        if current_user.is_admin:  # check admin  in session/ decorator property model User
            return "Привет админ"
        else:
            return "Ты кто?" 
    
        



    return app


