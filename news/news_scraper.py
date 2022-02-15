from django.db import IntegrityError
from .models import Newspaper
from bs4 import BeautifulSoup as bs
import requests, sys
import dateutil.parser
import logging, re

logging.basicConfig(filename='crawler.log', level=logging.INFO)

def scraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    VANGUARD_LIMIT = 10 # 35 posts are present, that's too much bandwidth wise, moreover they will be scraped before it gets pushed down the stack.
    sites =  ('the punch', 'the nation', 'the vanguard')
    # sites = ('the guardian', )
    posts = []
    
    if 'the guardian' in sites:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            page = requests.get("https://guardian.ng/", headers=headers)
            page = bs(page.content, 'lxml')
            regex = re.compile(r'(\bad\b|_ad|ad_)')
            for enum, i in enumerate(page.select('section.title-latest .design-article.item .title a')):
                post_url = i.get('href')
                post = requests.get(post_url, headers=headers)
                post = bs(post.content, 'lxml')
                
                for i in post.select('.article-header .subhead .date'):
                    published = i.text.split('|')[0].strip()
                    
                for i in post.select('.article-header .title'):
                    title = i.text
                    
                thumbnail_url = None
                for i in post.select('.article-header img'):
                    thumbnail_url = i.attrs.get('src')
                    
                post.select('.article-header')[0].decompose()
                html = ''
                for i in post.select('div.content article'):
                    for j in i.findAll():
                        try:
                            class_ = j.attrs.get("class")
                        except AttributeError: # because of decompose(), to remove ads widget
                            pass
                            
                        if (class_) and any([regex.findall(klass) for klass in class_]):
                            # if a class group is present and is of type article-header
                            # or contains ad as a word not as part of a word
                            j.decompose()
                        else:
                            html += str(j)            
                
                post = Newspaper(name=Newspaper.TG, title=title, 
                                 slug=post_url.split(Newspaper.TG_BASE)[1][1:-1],
                                 post_thumbnail = thumbnail_url,
                                 html = html,
                                 published=published,
                                 url = post_url,
                        ) # [1:-1] to remove the leading and trailing slash
                posts.append(post)
                
        except Exception as e: # there might be changes in things from there end
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(f"Exception type: {exc_type}, line-no: {exc_tb.tb_lineno}")                
            
    if 'the nation' in sites:
        try:
            page = requests.get('https://thenationonlineng.net/news-update/', headers=headers)
            parsed_page = bs(page.content, 'lxml')
            for i in parsed_page.select('.listing-blog article.type-post a[title]'):
                if i.attrs["title"].lower() != "Browse Author Articles".lower():
                    post_url = i.attrs["href"]
                    fp = requests.get(post_url, headers=headers)
                    parsed_post = bs(fp.content, 'lxml')
                    for i in parsed_post.select('.single-post-meta time b'):
                        published = i.text
                    thumbnail_url = None
                    for i in parsed_post.select('a.post-thumbnail'):
                        thumbnail_url = i.get('href')
                    for i in parsed_post.select('span.post-title'):
                        title = i.text
                    html = ''
                    for i in parsed_post.select('div.single-post-content'):
                        for j in [i.find_all('p', class_=None), i.find_all('p', class_="MsoNormal")]:
                            html += str(j)
                if not thumbnail_url:
                    continue
                post = Newspaper(name=Newspaper.TN, title=title, 
                                 slug=post_url.split(Newspaper.TN_BASE)[1][1:-1],
                                 post_thumbnail = thumbnail_url,
                                 html = html,
                                 published=published,
                                 url = post_url,
                        ) # [1:-1] to remove the leading and trailing slash
                posts.append(post)
        except Exception as e: # there might be changes in things from there end
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(f"Exception type: {exc_type}, line-no: {exc_tb.tb_lineno}")
            
    if 'the punch' in sites:
        page = requests.get('https://punchng.com/', headers=headers)
        parsed_page = bs(page.content, 'lxml')            
        try:
            for i in parsed_page.select('.list-timeline .entry-title a'):
                post_url = i.get("href")
                post = requests.get(post_url, headers=headers)
                page = bs(post.content, 'lxml')
                for i in page.select_one('span.entry-date span'):
                    published = i.text
                    
                for i in page.select('.entry-header .entry-title'):
                    title = i.text
                thumbnail_url = None
                for i in page.select('picture.entry-featured-image img'):
                    thumbnail_url = i.get('src')
                    
                html = ''
                for i in page.select('.entry-content'):
                    for j in i.find_all('p', class_=None):
                        html += str(j)
                        
                post = Newspaper(name=Newspaper.TP, title=title, 
                                 slug=post_url.split(Newspaper.TP_BASE)[1][1:-1],
                                 post_thumbnail = thumbnail_url,
                                 html = html,
                                 published = published,
                                 url = post_url,
                        ) # [1:-1] to remove the leading and trailing slash
                posts.append(post)
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(f"Exception type: {exc_type}, line-no: {exc_tb.tb_lineno}")
    
    if "the vanguard" in sites:
        try:
            url = "https://www.vanguardngr.com/"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            page = requests.get(url, headers=headers)
            page = bs(page.content, 'lxml')
            for enum, i in enumerate(page.select('ul.latest-news-list span.latest-news-title a')):
                
                if enum and enum == VANGUARD_LIMIT:
                    raise Exception
                    
                post_url = i.get('href')
                post = requests.get(post_url, headers=headers)
                post = bs(post.content, 'lxml')
                
                for i in post.select('span.posted-on time'):
                    published = dateutil.parser.isoparse(i.attrs.get('datetime')).date()
                
                for i in post.select('header h1.entry-title'):
                    title = i.text.strip()
                
                thumbnail_url = None # so as to prevent the previous one from being used, reassign.
                for i in [post.select('.entry-content figure>img'), post.select('.entry-content p img')]:
                    if i: # yo u gotta catch this in case
                        thumbnail_url = i[0].get('src')
                    
                html = ""
                for i in post.select('.entry-content'):
                    for j in i.find_all('p', class_=None):
                        html += str(j)
                
                post = Newspaper(name=Newspaper.TV, title=title, 
                     slug=post_url.split(Newspaper.TV_BASE)[1][1:-1],
                     post_thumbnail = thumbnail_url,
                     html = html,
                     published = published,
                     url = post_url,
                ) # [1:-1] to remove the leading and trailing slash
                posts.append(post)
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error(f"Exception type: {exc_type}, line-no: {exc_tb.tb_lineno}")
            
    if posts:
        for post in posts:
            if not post.html:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.info(f"HTML Empty; with url: {post.url}")
            try:
                post.save()
            except IntegrityError as e: # this is to be expected there are overlaps between newly scraped news and those in the database
                exc_type, exc_obj, exc_tb = sys.exc_info()