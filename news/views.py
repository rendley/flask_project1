from flask import Blueprint
from flask import Flask
from flask import render_template
from app.news_python_org import get_data_news
from app.db import db
from app.news.models import News

from flask import abort


blueprint = Blueprint("news",__name__, url_prefix="/news" )



@blueprint.route('/')
def news():
    title = "Новости"
    content_title = "Новости Python"
    news_list = get_data_news()     
    return render_template ("news/news.html", title=title, 
                            newslist=news_list, content_title=content_title
                            )
# all news
@blueprint.route('/news')
def news_habr():
    title = "Новости Python"
    content_title = "Новости Python Habr"
    news_habr = News.query.order_by(News.published.desc()).all() # sorted news / revers .asc()
    return render_template ("news/news_habr.html", title=title, 
                            news_habr=news_habr, content_title=content_title
                            )
# <int:news_id> - magic Flask not think
@blueprint.route("/news/<int:news_id>") 
def single_news(news_id):
    title = "Новости Python"
    my_news = News.query.filter(News.id == news_id).first()
    if not my_news: 
        abort(404)  # check 
    return render_template("news/text_news.html", title=title, 
                            content_title=my_news.title, news=my_news)