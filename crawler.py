import requests, sys
from bs4 import BeautifulSoup as bs
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
url = 'https://punchng.com/'
# url = 'https://thenationonlineng.net/ex-agitators-hail-dikio-for-repositioning-amnesty-programme/'
page = requests.get(url, headers=headers)
parsed_page = bs(page.content, 'lxml')
# print(soup.prettify())

for i in parsed_page.select('.list-timeline .entry-title a'):
    print('in loop')
    post_url = i.get("href")
    post = requests.get(post_url, headers=headers)
    page = bs(post.content, 'lxml')
    for i in page.select_one('span.entry-date span'):
        published = i
        print("The punch", published)
    for i in page.select('.entry-header .entry-title'):
        title = i.text
        print(title)
        
    for i in page.select('picture.entry-featured-image img'):
        thumbnail_url = i.get('src')
        
    # html = ''
    # for i in page.select('.entry-content'):
    #     for j in i.find_all('p', class_=None):
    #         html += str(j)
    
# for i in soup.select('.list-timeline .entry-title a'):
#     post_url = i.get("href")
#     post = requests.get(post_url, headers=headers)
#     page = bs(post.content, 'lxml')
#     for i in page.select('.entry-header .entry-title'):
#         print(i.text)
#     for i in page.select('.entry-content'):
#         for j in i.find_all('p', class_=None, style=None):
#             print(j)
#     for i in page.select('picture.entry-featured-image img'):
#         thumbnail = i.get('src')
#     print(thumbnail)
#     print()