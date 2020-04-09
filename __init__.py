from flask import Flask
import app.config
from flask import render_template
from app.weather import weather_by_city
from app.news import get_data_news
from app.model import db
from flask import current_app

def create_app(): 
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route('/')
    def index():
        title = "Flask"
        conent_title = "Flask Blog"
        return render_template ("index.html", title=title, conent_title=conent_title)

    @app.route('/news')
    def news():
        title = "Новости"
        conent_title = "Новости Python"
        news_list = get_data_news()
        weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
        return render_template ("news.html", title=title, weather=weather, 
                                newslist=news_list, conent_title=conent_title
                                )


    return app


