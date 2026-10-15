from datetime import date
from hijr_cal.models import EventOccurrence, Events
from hijr_cal.services import (
    save_hijri_cal,
    create_hijri_date_occurrence,
    create_hijri_range_occurrences,
    create_every_hijri_month_occurrences,
    create_weekday_occurrences,
    create_daily_occurrences,
    create_hijri_month_occurrences,
    load_events_from_json,
    fetch_and_save_events
)
from prayers.services import save_prayer_data
from members.models import Member
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SUNNAH_EVENTS_FILE = BASE_DIR /'data' / 'sunnah_acts.json'
HOLIDAY_EVENTS_FILE = BASE_DIR /'data' / 'holiday_events.json'
    


def refresh_global_data():
    today = date.today()

    # -------------------------
    # 1. HIJRI CALENDAR
    # -------------------------
    
    print("\n============================")
    print("REFRESH GLOBAL DATA")
    print("============================")


    print("\n1. Saving Hijri calendar...")
    save_hijri_cal(
        start_month=today.month,
        year=today.year
    )
    
    print("✓ Hijri calendar saved")


    print("\n2. Saving prayer data...")
    
    # ==================================
    # 1B. LOAD EVENT DEFINITIONS
    # ==================================

    print(
        "\n2. Loading Sunnah event definitions..."
    )

    print(
        "JSON path:",
        SUNNAH_EVENTS_FILE
    )

    print(
        "JSON exists:",
        SUNNAH_EVENTS_FILE.exists()
    )


    load_events_from_json(
        SUNNAH_EVENTS_FILE
    )
    
    


    print(
        "✓ Event definitions loaded"
    )

    print(
        "Events count:",
        Events.objects.count()
    )
    
    # ==================================
    # 1C. LOAD EVENT DEFINITIONS
    # ==================================

    print(
        "\n2. Loading Holiday event definitions..."
    )

    print(
        "JSON path:",
        HOLIDAY_EVENTS_FILE
    )

    print(
        "JSON exists:",
        HOLIDAY_EVENTS_FILE.exists()
    )


    load_events_from_json(
        HOLIDAY_EVENTS_FILE
    )
    
    print(
    "\n3. Loading Islamic holidays..."
)

    fetch_and_save_events()


    print(
        "✓ Event definitions loaded"
    )

    print(
        "Events count:",
        Events.objects.count()
    )



    # -------------------------
    # 2. PRAYER DATA
    # -------------------------
    locations = (
        Member.objects
        .exclude(city="")
        .exclude(country="")
        .values("city", "country", "madhab")
        .distinct()
    )

    for location in locations:
        city = location["city"]
        country = location["country"]
        madhab = location["madhab"]

        save_prayer_data(
            city=city,
            madhab=madhab,
            st_month=today.month,
            year=today.year,
            country=country
        )
        
    print("✓ Prayer data saved")


    print("\n3. Creating event occurrences...")

    # -------------------------
    # 3. EVENT OCCURRENCES
    # -------------------------
    print(
        "\n3. Creating event occurrences..."
    )


    create_hijri_date_occurrence()

    print(
        "After HIJRI_DATE:",
        EventOccurrence.objects.count()
    )


    create_hijri_range_occurrences()

    print(
        "After HIJRI_RANGE:",
        EventOccurrence.objects.count()
    )


    create_every_hijri_month_occurrences()

    print(
        "After EVERY_HIJRI_MONTH:",
        EventOccurrence.objects.count()
    )


    create_weekday_occurrences()

    print(
        "After WEEKDAY:",
        EventOccurrence.objects.count()
    )


    create_daily_occurrences()

    print(
        "After DAILY:",
        EventOccurrence.objects.count()
    )


    create_hijri_month_occurrences()

    print(
        "After HIJRI_MONTH:",
        EventOccurrence.objects.count()
    )

    
    print("✓ Occurrence creation finished")


    
    print(
        "EventOccurrence count:",
        EventOccurrence.objects.count()
    )


    print("============================\n")
    
    
    # ==================================
    # FINAL COUNTS
    # ==================================

    print("\n================================")
    print("GLOBAL REFRESH RESULTS")
    print("================================")

    print(
        "Events:",
        Events.objects.count()
    )

    print(
        "EventOccurrences:",
        EventOccurrence.objects.count()
    )

    print("================================\n")