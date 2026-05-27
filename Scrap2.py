
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
KEYWORDS += [word.title() for word in KEYWORDS]

headers = Headers(browser='chrome', os='win').generate()
url = 'https://habr.com/ru/all/'

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Ошибка при запросе: {e}")
    exit()

soup = BeautifulSoup(response.text, 'lxml')
articles = soup.select('article.tm-articles-list__item')

parsed_articles = []

for article in articles:
    time_tag = article.select_one('time')
    title_tag = article.select_one('h2')
    link_tag = article.select_one('a.tm-title__link')

    
    if not (title_tag and link_tag and time_tag):
        continue


    # берём весь текст внутри карточки статьи
    card_text = article.get_text(separator=' ', strip=True)

    time = time_tag['datetime']
    title = title_tag.text.strip()
    link = 'https://habr.com' + link_tag['href']


    # проверяем наличие ключевого слова в тексте
    if any(word in card_text for word in KEYWORDS):
        parsed_articles.append({
            'time': time,
            'title': title,
            'link': link
        })

# вывод

for item in parsed_articles:
    if isinstance(item, dict):
        print("<"+item["time"]+">", " - ", "<"+item["title"]+">", " - ", "<"+item["link"]+">")

#pprint(parsed_articles)

# сохранение
with open('article.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_articles, f, ensure_ascii=False, indent=4)


#<дата> - <заголовок> - <ссылка>