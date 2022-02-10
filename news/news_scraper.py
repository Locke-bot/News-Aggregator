from django.db import IntegrityError
from .models import Newspaper
from bs4 import BeautifulSoup as bs
import requests

def scraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    print("entering now")
    sites = ('the punch', 'the nation')
    posts = []
    if 'the nation' in sites:
        try:
            page = requests.get('https://thenationonlineng.net/news-update/', headers=headers)
            parsed_page = bs(page.content, 'lxml')
            for i in parsed_page.select('.listing-blog article.type-post a[title]'):
                print('in loop')
                if i.attrs["title"].lower() != "Browse Author Articles".lower():
                    print('actual shit')
                    post_url = i.attrs["href"]
                    fp = requests.get(post_url, headers=headers)
                    parsed_post = bs(fp.content, 'lxml')
                    for i in parsed_post.select('a.post-thumbnail'):
                        thumbnail_url = i.attrs['href']
                    
                    for i in parsed_post.select('span.post-title'):
                        title = i.text
                    html = ''
                    for i in parsed_post.select('div.single-post-content'):
                        for j in i.find_all('p', class_=None):
                            html += str(j)
                post = Newspaper(name=Newspaper.TN, title=title, 
                                 slug=post_url.split(Newspaper.TN_BASE)[1][1:-1],
                                 post_thumbnail = thumbnail_url,
                                 html = html
                        ) # [1:-1] to remove the leading and trailing slash
                posts.append(post)
        except Exception as e:
            print(f"{Newspaper.TN} Error: {e}")
        if posts:
            empty = 0
            for post in posts:
                if not post.html:
                    print("Empty Page")
                    empty += 1
                    continue
                try:
                    post.save()
                except IntegrityError:
                    pass
            print(f"{len(posts)} from {Newspaper.TN} of which {empty} is empty")
            
    if 'the punch' in sites:
        page = requests.get('https://punchng.com/', headers=headers)
        parsed_page = bs(page.content, 'lxml')            
        try:
            for i in parsed_page.select('.list-timeline .entry-title a'):
                print('in loop')
                post_url = i.get("href")
                post = requests.get(post_url, headers=headers)
                page = bs(post.content, 'lxml')
                for i in page.select('.entry-header .entry-title'):
                    title = i.text
                    
                for i in page.select('picture.entry-featured-image img'):
                    thumbnail_url = i.get('src')
                    
                html = ''
                for i in page.select('.entry-content'):
                    for j in i.find_all('p', class_=None, style=None):
                        html += str(j)
                        
                post = Newspaper(name=Newspaper.TP, title=title, 
                                 slug=post_url.split(Newspaper.TP_BASE)[1][1:-1],
                                 post_thumbnail = thumbnail_url,
                                 html = html
                        ) # [1:-1] to remove the leading and trailing slash
                posts.append(post)
        except Exception as e:
            print(f"{Newspaper.TP} Error: {e}")
    if posts:
        empty = 0
        for post in posts:
            if not post.html:
                empty += 1
                print("Empty Page")
                continue
            try:
                post.save()
            except IntegrityError:
                pass
        print(f"{len(posts)} from {Newspaper.TP} of which {empty} is empty")