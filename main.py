import bs4
import requests
from fake_headers import Headers

def get_full_text(node):
    text_div = node.find('div', class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
    paragraphs = text_div.find_all('p') if text_div else []
    return ' '.join([p.get_text() for p in paragraphs])

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'поиск', 'API', "Wild Hunt"]
URL = "https://habr.com"

response = requests.get(URL + "/ru/articles", headers=Headers(browser="chrome", os="mac").generate())
soup = bs4.BeautifulSoup(response.text, features="lxml")
articles_list = soup.find_all("article", class_=["tm-articles-list__item"])

result_list = []

for article in articles_list:
    article_href_node = article.find("a", attrs={"class": "tm-title__link", "data-article-link": "true"})
    article_link = URL + article_href_node["href"]
    article_title = article_href_node.find("span").text.strip()
    article_time = article.find("time")["datetime"]

    article_preview_text = get_full_text(article)

    full_article = requests.get(article_link)
    full_article_soup = bs4.BeautifulSoup(full_article.text, features="lxml")
    full_article_text = get_full_text(full_article_soup)

    for word in KEYWORDS:
        if word in article_preview_text or word in full_article_text:
            item = article_time + " – " + article_title.replace(u'\xa0', ' ') + " – " + article_link
            if item not in result_list:
                result_list.append(item)


for result in result_list:
    print(result)