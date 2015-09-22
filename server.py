import bottle
import waitress
import controller
import breathe
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler

bottle_app = bottle.app()
scheduler = BackgroundScheduler()
scheduler.configure(timezone=timezone('US/Pacific'))
breather = breathe.Breathe()
my_controller = controller.Controller(bottle_app, breather)


@scheduler.scheduled_job(trigger='cron', hour=19, minute=0)
def on_job():
    """Start at 7:00pm PT"""
    print('STARTING BREATHER')
    breather.restart()


@scheduler.scheduled_job(trigger='cron', hour=21, minute=0)
def off_job():
    """End at 9:00pm PT"""
    print("STOPPING BREATHER")
    breather.shutdown()

if __name__ == '__main__':
    scheduler.start()
    waitress.serve(bottle_app, host='0.0.0.0', port=7000)
