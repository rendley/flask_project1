from flask import Flask
import config
from flask import render_template
from weather import weather_by_city
from news import get_data_news

from flask import current_app

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def index():
    title = "Новости"
    news_list = get_data_news()
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    return render_template ("index.html", title=title, weather=weather, newslist=news_list)

if __name__ == '__main__':
    app.run()

