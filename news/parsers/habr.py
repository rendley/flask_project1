from bs4 import BeautifulSoup

from app.news.parsers.utils import get_html, save_news 

from datetime import datetime, timedelta 
import locale 
import platform 

from app.news.models import News 
from app.db import db 

# settings locale
if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian") # устанавливаем локаль для виндовс
else:
    locale.setlocale(locale.LC_ALL, "ru_RU")

# change time
# "29 марта 2020 в 15:35" return 29 Март 2020 в 15:35
def now_time(time):
    time_lst = time.split()
    what = ["января", "февраля", "марта", "апреля", "июня", "июля",
            "августа", "сентября", "октября", "ноября", "декабря"
            ]
    whereby = ["Январь", "Февраль", "Март", "Апрель", "Июнь", "Июль",
               "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
               ]
    repl_dict = dict(zip(what, whereby))
    return " ".join([repl_dict[x] if x in repl_dict else x for x in time_lst])

# convert "сегодня, вчера" in datetime
def get_news_date(date_str): 
    if "сегодня" in date_str:
        today = datetime.now()
        date_str = date_str.replace("сегодня", today.strftime("%d %B %Y")) # сегодня меняем на - день месяц год
    elif "вчера" in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace("вчера", yesterday.strftime("%d %B %Y"))
    try:
        date_str = now_time(date_str) 
        return datetime.strptime(date_str,"%d %B %Y в %H:%M") # str in datetime
    except ValueError:
        return datetime.now()

# parsing site
def get_habr_snippets():
    html = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find("ul", class_="content-list content-list_posts shortcuts_items").findAll("li")
        result_news = []
        for news in all_news:
            try:
                title = news.find("a", class_="post__title_link").text
            except:
                title = ""
            try:
                url = news.find("a", class_="post__title_link")["href"]
            except:
                url = ""
            try:
                published = news.find("span", class_="post__time").text
                published = get_news_date(published)
            except:
                published = ""
            if len(title) or len(url) or len(published): # delete empty str
                save_news(title, url, published)

# save text news
# is_None lets to collete with Null in database text
# text in database is_None == Null
# decode_contents = html with tags 
def get_habr_content(): 
    news_without_text = News.query.filter(News.text.is_(None)) 
    for news in news_without_text: 
        html = get_html(news.url)
        if html: 
            soup = BeautifulSoup(html, "html.parser")
            news_text = soup.find("div", class_= "post__text-html").decode_contents() 
            if news_text:
                news.text = news_text 
                db.session.add(news)
                db.session.commit()

