from apscheduler.schedulers.background import BackgroundScheduler
from priceUpdater.getPricesApi import func

sched = BackgroundScheduler()

@sched.scheduled_job('interval', seconds=30)
def timed_job():
    print('This job is run every three minutes.')

sched.start()