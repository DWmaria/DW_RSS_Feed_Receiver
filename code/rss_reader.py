import json

import requests

from bs4 import BeautifulSoup

def dw_english_topStories_rss():
    article_list = []
    try:
        r = requests.get('https://rss.dw.com/rdf/rss-de-all')
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('dc:date').text
            language = a.find('dc:language').text
            oid = a.find('dwsyn:contentID').text
            article = {
                'oid': oid,
                'title': title,
                'link': link,
                'published': published,
                'language': language
            }
            article_list.append(article)
        print(len(article_list))
        return save_to_txt(article_list)

    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)

def save_to_txt(article_list):
    with open('articles.txt', 'w') as f:
        for a in article_list:
            json.dump(a, f, indent=2)
        f.close()

print('Starting scraping')
dw_english_topStories_rss()
print('Finished scraping')