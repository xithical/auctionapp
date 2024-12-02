import time

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app.classes.models.events import Events_Methods
from app.classes.models.main_cart import MainCart_Methods

from app.classes.controllers.checkout import Checkout_Controller

from app.classes.helpers.init_helpers import Init_Helpers
from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.email_helpers import Email_Helpers
from app.classes.helpers.payments_helpers import Payments_Helpers

Init_Helpers.init_db()

scheduler = BackgroundScheduler()
    
def end_event(event_id: int):
    carts = MainCart_Methods.get_all_carts_for_event(event_id)

    for cart in carts:
        cart_summary = Checkout_Controller.get_cart(cart["user_id"]["user_id"], cart["event_id"]["event_id"])
        amount = cart_summary["auction_items"]["price_total"] + cart_summary["merch_items"]["price_total"]
        if amount > 0:
            payment = Payments_Helpers.charge_cart(cart["cart_id"])
            if payment is not None:
                Email_Helpers.Senders.event_receipt(cart["user_id"]["user_id"], cart["event_id"]["event_id"])
            else:
                print(f'{__name__} - failed to send receipt for {cart["user_id"]["user_id"]}')
    print(f"{__name__} - Ended event {event_id} and charged cards where applicable")

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
        try:
            db_event = Events_Methods.get_event_by_id(event_id)
            schedule_time = (event.next_run_time).replace(tzinfo=None)
            if not db_event.end_time == schedule_time:
                scheduler.reschedule_job(f'event_{event_id}', trigger='date', run_date=db_event.end_time)
                print(f'Rescheduled {event.id}, \"{db_event.event_name}\" from {schedule_time} to {db_event.end_time}')
        except Exception as e:
            print(f"{__name__} - Couldn't get event for schedule {event.id}, removing scheduled task: {e}")
            scheduler.remove_job(event.id)

if __name__ == '__main__':
    scheduler.start()
    init_scheduler(scheduler)
    print("Started scheduler")
    while True:
            time.sleep(1)
            check_new_events(scheduler)
            update_events(scheduler)