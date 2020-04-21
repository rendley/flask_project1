import requests
from app.db import db  # потребуется чтобы записать новость сразу в базу данных
from app.news.models import News


def get_html(url): 
    headers = { "User-Agent": "UserMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    } 
    try:
        result = requests.get(url, headers=headers) 
        result.raise_for_status()  
        return result.text  
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка!")
        return False


def save_news(title, url, published): 
    news_exists = News.query.filter(News.url == url).count()  
    print(news_exists)
    if not news_exists: 
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news) 
        db.session.commit()
