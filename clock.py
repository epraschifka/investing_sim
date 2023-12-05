from apscheduler.schedulers.blocking import BlockingScheduler
from priceUpdater.getPricesApi import update_prices

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    update_prices.func()

sched.start()