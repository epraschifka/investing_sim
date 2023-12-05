# updater.py
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from priceUpdater import getPricesApi

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getPricesApi.func, "interval", seconds=20)
    scheduler.start()

if __name__ == "__main__":
    start()
