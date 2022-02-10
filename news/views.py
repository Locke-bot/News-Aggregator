from itertools import chain

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
        name = ' '.join([i.capitalize() for i in name.split('-')])
        obj = self.get_object(name, number)
        if not obj: # check if it is a queryset instance
            return Response({"error": str(obj)})
        serializer = NewsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    