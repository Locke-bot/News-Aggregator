from django.contrib import admin
from .models import Newspaper
# Register your models here.

class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "title", "created_at", "published")
    list_display_links = list_display

admin.site.register(Newspaper, NewspaperAdmin)
