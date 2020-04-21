from flask import Blueprint
from flask import Flask
from flask import render_template
from app.news_python_org import get_data_news
from app.db import db
from app.news.models import News


blueprint = Blueprint("news",__name__, url_prefix="/news" )



@blueprint.route('/')
def news():
    title = "Новости"
    content_title = "Новости Python"
    news_list = get_data_news()     
    return render_template ("news/news.html", title=title, 
                            newslist=news_list, content_title=content_title
                            )

@blueprint.route('/python')
def news_habr():
    title = "Новости Python"
    content_title = "Новости Python"
    news_habr = News.query.all()    
    return render_template ("news/news_habr.html", title=title, 
                            news_habr=news_habr, content_title=content_title
                            )