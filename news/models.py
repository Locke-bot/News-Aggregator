from django.db import models
from urllib import parse
from bs4 import BeautifulSoup as bs

# Create your models here.

class Newspaper(models.Model):
    TN, TP, TV = "The Nation", "The Punch", "The Vanguard"
    TN_BASE = "https://thenationonlineng.net"
    TP_BASE = "https://punchng.com"
    name_url = {TN: TN_BASE, TP:TP_BASE}
    order = (TN, TP) # ascemnding order
    PAPER_CHOICES = (
            (TN, "The Nation"),
            (TP, "The Punch"),
            (TV, "The Vanguard"),
        )
    EXCERPT_LENGTH = 100
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20, choices=PAPER_CHOICES)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    post_thumbnail = models.URLField()
    html = models.TextField()
    excerpt = models.TextField(max_length=50)
    url = models.URLField(null=True)
    
    class Meta:
        get_latest_by = "-created_at"
    
    def get_excerpt(self):
        text = bs(self.html, 'lxml').text
        min_length = min(self.EXCERPT_LENGTH, len(text)) # bounded by the length of the article
        excerpt = text[:min_length]
        if len(text) > self.EXCERPT_LENGTH: # just three dots
            return excerpt.rstrip('.')+'...'
        return excerpt

    def get_url(self):
        return parse.urljoin(self.name_url[self.name], self.slug)

    def save(self, *args, **kwargs):
        self.excerpt = self.get_excerpt()
        self.url = self.get_url()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
