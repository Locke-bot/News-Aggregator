from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .news_scraper import scraper

def start():
    print("starting schedule")
    scheduler = BackgroundScheduler()
    # scheduler.add_job(scraper, 'interval', minutes=1)
    scheduler.add_job(scraper, 'interval', seconds=5)
    scheduler.start()