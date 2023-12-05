from apscheduler.schedulers.background import BackgroundScheduler
from priceUpdater.getPricesApi import update_prices

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    update_prices.func()

sched.start()