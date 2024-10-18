import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import random

import httpx

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def data_fill():
    employee = {
    "first_name": "John" + str(random.randint(0, 100)),
    "last_name": "Marston" + str(random.randint(0, 100)),
    "salary": 2000 + random.randint(0, 1000),
    "date_join": str(datetime.date.today()),
    "on_field": True if random.randint(0, 10) > 5 else False  
    }

    try:
        response = httpx.post(
            "http://localhost:8000/employees/",
            json=employee
        )
        
        if response.status_code == 201:
            print("Employee created successfully:", response.json(), flush=True)
        else:
            print(f"Failed to create employee: {response.status_code}", flush=True)
            print(response.text)
    except httpx.RequestError as e:
        print(f"An error occurred while requesting: {e}", flush=True)

def start():
    scheduler.add_job(
        data_fill,  
        trigger=IntervalTrigger(seconds=10), 
        id="my_job_id",
        max_instances=1, 
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started.")

def stop():
    scheduler.shutdown()
