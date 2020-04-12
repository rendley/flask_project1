from flask import Flask
import app.config
from flask import render_template
from app.weather import weather_by_city
from app.news import get_data_news
from app.model import db
from app.forms import LoginForm
from flask import current_app

def create_app(): 
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

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
    
    @app.route("/login")
    def login():
        title = "Авторизация"
        form = LoginForm()
        return render_template("login.html", form=form, title=title)


    return app


