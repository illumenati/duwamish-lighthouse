import bottle
from cso_parser import CsoParser
import waitress
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from breathe import Breathe
from controller import Controller

bottle_app = bottle.app()
scheduler = BackgroundScheduler()
scheduler.configure(timezone=timezone('US/Pacific'))
breather = Breathe()
requested = {"KDOM.CSOSTATUS_N", "HARB.CSOSTATUS_N", "CHEL.CSOSTATUS_N", "LAND.CSOSTATUS_N", "HANF.CSOSTATUS_N",
             "DUWA.CSOSTATUS_N", "BRAN.CSOSTATUS_N", "T115.CSOSTATUS_N", "MICH.CSOSTATUS_N", "WMIC.CSOSTATUS_N",
             "EMAR.CSOSTATUS_N", "8TH.CSOSTATUS_N", "NORF.CSOSTATUS_N", "NPDES078", "NPDES080", "NPDES107", "NPDES116"}
cso_parser = CsoParser(requested)
my_controller = Controller(bottle_app, breather)


@scheduler.scheduled_job(trigger='cron', hour=17, minute=30)
def on_job():
    """Start at 7:00pm PT"""
    print('STARTING BREATHER')
    breather.restart()


@scheduler.scheduled_job(trigger='cron', hour=19, minute=30)
def off_job():
    """End at 9:00pm PT"""
    print("STOPPING BREATHER")
    breather.stop()


@scheduler.scheduled_job(trigger='cron', hour=1, minute=30)
def cso_job():
    """Get CSO data at 1:30am and update the breather with the current status."""
    print("Fetch CSO status and update breather.")
    cso_parser.update()

    if cso_parser.now_count or cso_parser.recent_count:
        breather.erratic()
    else:
        breather.calm()

if __name__ == '__main__':
    scheduler.start()
    waitress.serve(bottle_app, host='0.0.0.0', port=7000)
