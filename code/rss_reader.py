import json

import requests

from bs4 import BeautifulSoup


def dw_english_topStories_rss():
    article_list = []
    #nicht gefunden: bengali, bulgarisch, kroatisch griechisch hindi kiswahili mazedonisch urdu
    language_list = ['en-all', 'de-all', 'alb-all', 'amh-news', 'ar-all', 'bos-all', 'chi-all',
                     'dar-all', 'fre-all',  'br-africa','sp-all', 'hau-nr', 'ind-all', 'pas-all',
                     'per-all', 'pol-all', 'br-all', 'rom-all', 'ru-all', 'serbian_all',  'tur-all',
                     'ukr-all']

    try:
        for lang in language_list:
                frag = ''
                if lang != 'serbian_all': frag = 'rss-'
                url = 'https://rss.dw.com/rdf/'+frag+lang
                r = requests.get(url)
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
                print(lang + ': ' + str(len(articles)))
        save_to_txt(article_list)
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