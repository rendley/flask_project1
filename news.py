import requests
from bs4 import BeautifulSoup
from datetime import datetime



def get_html(url): 
    try:
        result = requests.get(url)
        result.raise_for_status() 
        return result.text  
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка!")
        return False


def get_data_news():   
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, "html.parser") 
        all_news = soup.find("ul", class_="list-recent-posts")
        all_news = all_news.findAll("li")
        result_news = []
        for news in all_news:
            title = news.find("a").text            
            url = news.find("a")["href"]
            published = news.find("time").text
            try:
                published = datetime.strptime(published, "%Y-%m-%d")# парсит строку по формату который мы задали
            except ValueError:
                published = datetime.now()
            result_news.append({
                "title": title,
                "url": url,
                "published": published
            })
        return result_news
    return False    




if __name__ == "__main__":
    get_data_news()