from .models import Hijr_cal, EventOccurrence, Events
from datetime import datetime
from .helpers import get_hijr_cal, get_islamic_events
from django.utils.text import slugify
import json

def format_date(date_str):
    return datetime.strptime(
        date_str,
        "%d-%m-%Y"
    ).date()


def save_hijri_month(month, year):
    calendar = get_hijr_cal(month, year)

    for day in calendar:
        Hijr_cal.objects.update_or_create(
            gregorian_date=format_date(
                day["gregorian_date"]
            ),

            defaults={
                "hijri_day": int(
                    day["hijri_day"]
                ),

                "hijri_month": int(
                    day["hijri_month"]
                ),

                "hijri_year": int(
                    day["hijri_year"]
                ),

                "hijri_month_name":
                    day["hijri_month_name"]
            }
        )
        
def save_hijri_cal(
    start_month,
    year
):
    for month in range(
        start_month,
        13
    ):
        save_hijri_month(
            month,
            year
        )
        

def save_api_events(api_data):
    events = api_data["data"]["events"]

    for item in events:

        name = item["name"]

        event_defaults = {
            "name": name,
            "event_type": "HOLIDAY",
            "date_type": "HIJRI_DATE",

            "hijri_month": item["month"],
            "hijri_day": item["day"],
            "hijri_end_day": None,

            "weekday": None,

            "time_type": "ALL_DAY",
            "reference_prayer": None,

            "offset_minutes": 0,
            "duration_minutes": None,

            "description": item["description"],

            "moon_sighting_sensitive": True,
        }
        
        if name == "Laylat al-Qadr window begins":
            event_defaults["name"] = "Last Ten Nights of Ramadan"
            event_defaults["date_type"] = "HIJRI_RANGE"
            event_defaults["hijri_day"] = 21
            event_defaults["hijri_end_day"] = 30

        Events.objects.update_or_create(
            slug=slugify(
                event_defaults["name"]
            ),
            defaults=event_defaults
        )

def fetch_and_save_events():
    data = get_islamic_events()

    save_api_events(data)
    
def load_events_from_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        events = json.load(file)

    for item in events:

        data = item.copy()

        slug = data.pop("slug")

        Events.objects.update_or_create(
            slug=slug,
            defaults=data
        )
        
def create_hijri_date_occurrence():
    events = Events.objects.filter(date_type='HIJRI_DATE')
    
    for event in events:
        dates = Hijr_cal.objects.filter(hijri_month=event.hijri_month, hijri_day=event.hijri_day)
        
        for hijri_date in dates:
            EventOccurrence.objects.update_or_create(
                event=event,
                gregorian_date=hijri_date.gregorian_date,

                defaults={
                    "hijri_date": hijri_date,
                    "all_day": True,
                }
            )
            
def create_hijri_range_occurrences():
    events = Events.objects.filter(
        date_type="HIJRI_RANGE"
    )

    for event in events:
        dates = Hijr_cal.objects.filter(
            hijri_month=event.hijri_month,
            hijri_day__gte=event.hijri_day,
            hijri_day__lte=event.hijri_end_day
        )

        for hijri_date in dates:
            EventOccurrence.objects.update_or_create(
                event=event,
                gregorian_date=hijri_date.gregorian_date,
                defaults={
                    "hijri_date": hijri_date,
                    "all_day": True,
                }
            )
        
def create_every_hijri_month_occurrences():
    events = Events.objects.filter(
        date_type="EVERY_HIJRI_MONTH"
    )

    for event in events:
        dates = Hijr_cal.objects.filter(
            hijri_day__gte=event.hijri_day,
            hijri_day__lte=event.hijri_end_day
        )

        for hijri_date in dates:
            EventOccurrence.objects.update_or_create(
                event=event,
                gregorian_date=hijri_date.gregorian_date,
                defaults={
                    "hijri_date": hijri_date,
                    "all_day": True,
                }
            )
            

def create_weekday_occurrences():
    events = Events.objects.filter(
        date_type="WEEKDAY"
    )

    for event in events:
        dates = Hijr_cal.objects.all()

        for hijri_date in dates:
            if hijri_date.gregorian_date.weekday() != event.weekday:
                continue

            EventOccurrence.objects.update_or_create(
                event=event,
                gregorian_date=hijri_date.gregorian_date,
                defaults={
                    "hijri_date": hijri_date,
                    "all_day": event.time_type == "ALL_DAY",
                }
            )
            
def create_daily_occurrences():
    events = Events.objects.filter(
        date_type="DAILY"
    )

    dates = Hijr_cal.objects.all()

    for event in events:
        for hijri_date in dates:
            EventOccurrence.objects.update_or_create(
                event=event,
                gregorian_date=hijri_date.gregorian_date,
                defaults={
                    "hijri_date": hijri_date,
                    "all_day": event.time_type == "ALL_DAY",
                }
            )

def create_hijri_month_occurrences():
    events = Events.objects.filter(
        date_type="HIJRI_MONTH"
    )

    for event in events:
        dates = Hijr_cal.objects.filter(
            hijri_month=event.hijri_month
        )

        for hijri_date in dates:
            EventOccurrence.objects.update_or_create(
                event=event,
                gregorian_date=hijri_date.gregorian_date,
                defaults={
                    "hijri_date": hijri_date,
                    "all_day": event.time_type == "ALL_DAY",
                }
            )