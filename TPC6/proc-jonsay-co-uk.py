#!usr/bin/python3

import re
import shelve
import requests
import jjcli
from bs4 import BeautifulSoup as bs

d = shelve.open('pagecache.db')
page_url = "https://natura.di.uminho.pt/~jj/bs4/folha8-2023/"

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
        title = article.find('h1', class_="entry-title")
        title = title.text if title else "No title found"
        entry_content = article.find('div', class_="entry-content")
        entry_content = entry_content.text if entry_content else "No content found"
        print(f"{id} :: {title}\n{entry_content}")

def get_article_links(url):
    text = myget(url)
    dt = bs(text, 'lxml')
    table = dt.find('table')
    all_links = []
    link_count = 0
    if table:
        for row in list(table.find_all('tr'))[3:]:
            for cell in row.find_all('td'):
                for link in cell.find_all('a'):
                    if link_count >= 20:
                        return all_links
                    if link['href'] == "__ARTS":
                        continue
                    url2 = url + link['href']
                    text = myget(url2)
                    dt = bs(text, 'lxml')
                    if not dt.find('article'):
                        get_article_links(url2)
                    else:
                        all_links.append(url2)
                        link_count += 1
    return all_links

def main():
    cl = jjcli.clfilter("s:")
    sep = cl.opt.get('-s', ' :: ') # without both these lines above, the output is not formatted as utf-8, why? I don't know
    urls = get_article_links(page_url)
    for url in urls:
        get_article_content(url)

if __name__ == "__main__":
    main()
    d.close()