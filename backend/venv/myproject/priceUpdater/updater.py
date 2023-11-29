from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from forecastUpdater import getPricesApi


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getPricesApi.func, "interval", seconds=30)
    scheduler.start()
