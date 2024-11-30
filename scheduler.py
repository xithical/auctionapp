import time

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app.classes.models.events import Events_Methods

from app.classes.helpers.init_helpers import Init_Helpers
from app.classes.helpers.config_helpers import Config_Helpers

Init_Helpers.init_db(scheduler=True)

scheduler = BackgroundScheduler()
    
def end_event(event_id: int):
    print(Events_Methods.get_event_by_id(event_id).event_name)

def init_scheduler(scheduler):
    events = Events_Methods.get_all_events()
    for event in events:
        if event["end_time"] > datetime.now():
            scheduler.add_job(func=end_event, trigger='date', id=f'event_{event["event_id"]}', run_date=event["end_time"], args=[event["event_id"]])
            print(f'Added schedule for event {event["event_id"]}, \"{event["event_name"]}\", on {event["end_time"]}')

def check_new_events(scheduler):
    events = Events_Methods.get_all_events()
    for event in events:
        if (event["end_time"] > datetime.now()) & (not scheduler.get_job(f'event_{event["event_id"]}')):
            scheduler.add_job(func=end_event, trigger='date', id=f'event_{event["event_id"]}', run_date=event["end_time"], args=[event["event_id"]])
            print(f'Added schedule for event {event["event_id"]}, \"{event["event_name"]}\", on {event["end_time"]}')

def update_events(scheduler):
    events = scheduler.get_jobs()
    for event in events:
        event_id = int(event.id.rsplit('_',1)[1])
        db_event = Events_Methods.get_event_by_id(event_id)
        schedule_time = (event.next_run_time).replace(tzinfo=None)
        if not db_event.end_time == schedule_time:
            scheduler.reschedule_job(f'event_{event_id}', trigger='date', run_date=db_event.end_time)
            print(f'Rescheduled {event.id}, \"{db_event.event_name}\" from {schedule_time} to {db_event.end_time}')


if __name__ == '__main__':
    scheduler.start()
    init_scheduler(scheduler)
    try:
        while True:
            time.sleep(1)
            check_new_events(scheduler)
            update_events(scheduler)
    except Exception as e:
        print(f"Halting scheduler: {e}")
        exit()
    finally:
        exit()