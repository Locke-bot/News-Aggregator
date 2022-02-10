from itertools import chain

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db import IntegrityError
from bs4 import BeautifulSoup as bs
from .models import Newspaper
import requests

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NewsSerializer
from rest_framework.permissions import IsAdminUser

# Create your views here.
    
class NewsListApi(APIView):
    
    def get(self, request, number, format=None):
        News = [] # capitalized!
        latest = Newspaper.objects.latest("created_at")
        News.append([latest])
        for name in Newspaper.order:
            # The very latest one for the main post uninfleunced by the no set in settings
            news = Newspaper.objects.exclude(pk = latest.pk).filter(name=name).order_by("-created_at")[:number]
            News.append(news)
        serializer = NewsSerializer(list(chain(*News)), many=True)
        return Response(serializer.data)
            
class NewsApi(APIView):
    
    def get_object(self, pk):
        try:
            return Newspaper.objects.get(pk=pk)
        except Newspaper.DoesNotExist:
            pass
    
    def get(self, request, pk, format=None):
        obj = self.get_object(pk) or None
        if not obj:
            return Response({"error": "object does not exist"})
        serializer = NewsSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SpecificNews(APIView): # specific newspaper

    def get_object(self, name, number):
        try:
            return Newspaper.objects.filter(name=name).order_by("-created_at")[:number]
        except Exception as e: # number might be too much, or name might be invalid
            return e
    
    def get(self, request, name, number, format=None):
        print(request, name, number) 
        name = ' '.join([i.capitalize() for i in name.split('-')])
        obj = self.get_object(name, number)
        if not obj: # check if it is a queryset instance
            return Response({"error": str(obj)})
        serializer = NewsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

def HomeView(request):
    # print(request.__dir__().__str__())
    # print(request.path)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    print("entering now")
    sites = ('the punch', 'the nation')
    if request.path == "/reload":
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
                for post in posts:
                    if not post.html:
                        print("Empty Page")
                        continue
                    try:
                        Newspaper.objects.create(post)
                    except IntegrityError:
                        pass
                print(len(posts), f" {Newspaper.TN}")
                
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
            for post in posts:
                if not post.html:
                    print("Empty Page")
                    continue
                try:
                    Newspaper.objects.create(post)
                except IntegrityError:
                    pass
            print(len(posts), f" {Newspaper.TP}")

    return TemplateResponse(request, "home.html", {"payload": Newspaper.objects.first().html})