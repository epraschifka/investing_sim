""" from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from priceUpdater import getPricesApi


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getPricesApi.func, "interval", minutes=5)
    scheduler.start()
 """