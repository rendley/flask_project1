from flask import Blueprint
from flask import Flask
from flask import render_template
from app.news_python_org import get_data_news
from app.db import db


blueprint = Blueprint("news",__name__, url_prefix="/news" )



@blueprint.route('/')
def news():
    title = "Новости"
    content_title = "Новости Python"
    news_list = get_data_news()     
    return render_template ("news/news.html", title=title, 
                            newslist=news_list, content_title=content_title
                            )
