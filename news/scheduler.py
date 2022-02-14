from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from .news_scraper import scraper

def start():
    print("starting schedule")
    scheduler = BackgroundScheduler()
    # scheduler.add_job(scraper, 'interval', minutes=settings.SCRAPE_INTERVAL)
    scheduler.add_job(scraper, 'date')
    scheduler.start()