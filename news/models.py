from django.db import models
from urllib import parse
from bs4 import BeautifulSoup as bs
from datetime import datetime

# Create your models here.

class Newspaper(models.Model):
    TG, TN, TP, TV = "The Guardian", "The Nation", "The Punch", "The Vanguard"
    TG_BASE = "https://guardian.ng/"
    TN_BASE = "https://thenationonlineng.net"
    TP_BASE = "https://punchng.com"
    TV_BASE = "https://www.vanguardngr.com"
    name_url = {TG: TG_BASE, TN: TN_BASE, TP:TP_BASE, TV:TV_BASE}
    order = (TG, TN, TP, TV) # ascending order
    PAPER_CHOICES = (
            (TG, TG),
            (TN, TN),
            (TP, TP),
            (TV, TV),
        )
    EXCERPT_LENGTH = 100
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20, choices=PAPER_CHOICES)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    post_thumbnail = models.URLField(null=True) # I had to add it because some vanguard posts don't have thumbnails
    html = models.TextField()
    excerpt = models.TextField(max_length=50)
    url = models.URLField(null=True)
    published = models.DateField()
    
    class Meta:
        get_latest_by = "-created_at"
    
    def get_excerpt(self):
        text = bs(self.html, 'lxml').text
        text = text.strip('[]') # seeing some artifacts in the html
        min_length = min(self.EXCERPT_LENGTH, len(text)) # bounded by the length of the article
        excerpt = text[:min_length]
        if len(text) > self.EXCERPT_LENGTH: # just three dots
            return excerpt.rstrip('.')+'...'
        return excerpt

    def parse_date(self, date):
        # so case changes doesn't break the code
        if self.name.lower() == "The Nation".lower():
            # the nation's date is of the form Feb 10, 2022
            return datetime.strptime(date, "%b %d, %Y").date()
        
        elif self.name.lower() in ("The Punch".lower(), "The Guardian".lower()):
            # the punch's date is of the form "01 February 2022"
            return datetime.strptime(date, "%d %B %Y").date()

    
    def save(self, *args, **kwargs):
        self.excerpt = self.get_excerpt()
        if type(self.published) is str:
            self.published = self.parse_date(self.published)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title