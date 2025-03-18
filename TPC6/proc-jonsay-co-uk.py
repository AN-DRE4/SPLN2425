#!usr/bin/python3

import re
import shelve
import requests
import jjcli
from bs4 import BeautifulSoup as bs

d = shelve.open('pagecache.db')
def myget(url):
    if url not in d:
        print("...getting url")
        d[url] = requests.get(url).text
    return d[url] 

def get_article_content(url):
    text = myget(url)
    dt = bs(text, 'lxml')
    for article in dt.find_all('article'):
        id = article['id']
        title = article.find('h1', class_="entry-title").text
        entry_content = article.find('div', class_="entry-content").text
        print(f"{id} :: {title}\n{entry_content}")

def main():
    cl = jjcli.clfilter("s:")
    sep = cl.opt.get('-s', ' :: ')
    for url in cl.args:
        get_article_content(url)

if __name__ == "__main__":
    main()
    d.close()