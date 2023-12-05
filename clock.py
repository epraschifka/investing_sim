from apscheduler.schedulers.background import BackgroundScheduler
from priceUpdater.getPricesApi import func

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    func()

sched.start()