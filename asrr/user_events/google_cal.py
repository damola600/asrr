from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from datetime import timedelta, time, datetime
from django.utils import timezone
from zoneinfo import ZoneInfo
import time as tm
from googleapiclient.errors import HttpError
from .models import GoogleCalendarConnection, UserEvent,PrayerGoogleEvent
from prayers.models import Prayer
from .prayer_services import build_user_prayer_events
import hashlib
import json


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_user_event_hash(user_event):
    event = user_event.occurrence.event
    occurrence = user_event.occurrence

    data = {
        "name": event.name,
        "description": event.description,
        "date": occurrence.gregorian_date.isoformat(),
        "all_day": user_event.all_day,

        "start_time": (
            user_event.start_time.isoformat()
            if user_event.start_time
            else None
        ),

        "end_time": (
            user_event.end_time.isoformat()
            if user_event.end_time
            else None
        ),

        "reminder_at": (
            user_event.reminder_at.isoformat()
            if user_event.reminder_at
            else None
        ),
    }

    event_string = json.dumps(
        data,
        sort_keys=True
    )

    return hashlib.sha256(
        event_string.encode()
    ).hexdigest()

def get_google_calendar_service(user):
    if not hasattr(user, "google_calendar_connection"):
        raise ValueError(
            "User has not connected Google Calendar."
        )

    connection = user.google_calendar_connection

    credentials = Credentials(
        token=connection.access_token,
        refresh_token=connection.refresh_token,
        token_uri=connection.token_uri,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=connection.scopes.split()
    )

    # Refresh token if access token expired
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

        connection.access_token = credentials.token
        connection.token_expiry = credentials.expiry

        connection.save(
            update_fields=[
                "access_token",
                "token_expiry"
            ]
        )

    service = build(
        "calendar",
        "v3",
        credentials=credentials
    )

    return service




def sync_one_event(user_event, service):
    event_body = build_event_body(user_event)

    if event_body is None:
        return None

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    user_event.google_event_id = created_event["id"]
    user_event.synced_to_google = True
    user_event.needs_google_sync = False
    user_event.last_synced_hash = get_user_event_hash(
        user_event
    )

    user_event.save(
        update_fields=[
            "google_event_id",
            "synced_to_google",
            "needs_google_sync",
            "last_synced_hash",
        ]
    )

    return created_event

def update_google_event(user_event, service):
    if not user_event.google_event_id:
        raise ValueError(
            "UserEvent does not have a Google event ID."
        )

    event_body = build_event_body(user_event)

    if event_body is None:
        return None

    updated_event = service.events().update(
        calendarId="primary",
        eventId=user_event.google_event_id,
        body=event_body
    ).execute()

    user_event.synced_to_google = True
    user_event.needs_google_sync = False
    user_event.last_synced_hash = get_user_event_hash(
        user_event
    )

    user_event.save(
        update_fields=[
            "synced_to_google",
            "needs_google_sync",
            "last_synced_hash",
        ]
    )

    return updated_event

def sync_user_calendar(user, batch_size=20):
    service = get_google_calendar_service(user)
    
    while True:

        events = UserEvent.objects.filter(
            user=user,
            needs_google_sync=True,
            pending_google_delete=False
        )[:batch_size]
        
        if not events:
            break
    
        print(
            "Total waiting:",
            UserEvent.objects.filter(
                user=user,
                needs_google_sync=True,
                pending_google_delete=False
            ).count()
        )
        
        print(
            "Normal events needing sync:",
            len(events)
        )

        for user_event in events:
            print(
                "Syncing event:",
                user_event.occurrence.event.name
                if hasattr(
                    user_event.occurrence,
                    "event"
                )
                else user_event.id
            )
            try:
                # Already exists in Google → UPDATE
                if user_event.google_event_id:
                    update_google_event(
                        user_event,
                        service
                    )

                # Does not exist in Google → CREATE
                else:
                    sync_one_event(
                        user_event,
                        service
                    )

                tm.sleep(0.1)

            except HttpError as e:
                error_text = str(e)

                if (
                    e.resp.status in [403, 429]
                    and "rateLimitExceeded" in error_text
                ):
                    print(
                        f"Rate limit hit for "
                        f"{user_event.occurrence.event.name}. "
                        f"Waiting 5 seconds..."
                    )

                    tm.sleep(5)

                    try:
                        if user_event.google_event_id:
                            update_google_event(
                                user_event,
                                service
                            )
                        else:
                            sync_one_event(
                                user_event,
                                service
                            )

                    except HttpError as retry_error:
                        print(
                            "Retry failed:",
                            user_event.occurrence.event.name,
                            retry_error
                        )

                else:
                    print(
                        "Failed:",
                        user_event.occurrence.event.name,
                        e
                    )

def get_user_event_timezone(user_event):
    member = user_event.user.profile
    event_date = user_event.occurrence.gregorian_date

    prayer = Prayer.objects.filter(
        date=event_date,
        city=member.city,
        country=member.country,
        madhab=member.madhab
    ).first()

    if prayer is None:
        raise ValueError(
            f"No prayer data found for "
            f"{member.city}, {member.country} "
            f"on {event_date}."
        )

    return prayer.timezone              
                
def build_event_body(user_event):
    event = user_event.occurrence.event
    occurrence = user_event.occurrence
    timezone_name = get_user_event_timezone(user_event)
    member = user_event.user.profile

    event_body = {
        "summary": event.name,
        "description": event.description,
    }

    # ALL-DAY EVENT
    if user_event.all_day:
        start_date = occurrence.gregorian_date
        end_date = start_date + timedelta(days=1)

        event_body["start"] = {
            "date": start_date.isoformat()
        }

        event_body["end"] = {
            "date": end_date.isoformat()
        }

        if user_event.reminder_at:
            event_start = datetime.combine(
                    start_date,
                    time.min,
                    tzinfo=ZoneInfo(timezone_name)
                )
            

            reminder_difference = (
                event_start - user_event.reminder_at
            )

            reminder_minutes = int(
                reminder_difference.total_seconds() / 60
            )

            if reminder_minutes > 0:
                event_body["reminders"] = {
                    "useDefault": False,
                    "overrides": [
                        {
                            "method": "popup",
                            "minutes": reminder_minutes
                        }
                    ]
                }

    # TIMED EVENT
    else:
        if user_event.start_time is None:
            return None

        end_time = user_event.end_time

        if end_time is None:
            end_time = (
                user_event.start_time
                + timedelta(minutes=30)
            )

        event_body["start"] = {
            "dateTime": user_event.start_time.isoformat(),
            "timeZone": timezone_name,
        }

        event_body["end"] = {
            "dateTime": end_time.isoformat(),
            "timeZone": timezone_name,
        }

    return event_body



def get_prayer_start_time(prayer_google_event):
    prayer = prayer_google_event.prayer
    name = prayer_google_event.prayer_name

    prayer_map = {
        "Fajr": prayer.fajr,
        "Dhuhr": prayer.dhuhr,
        "Asr": prayer.asr,
        "Maghrib": prayer.maghrib,
        "Isha": prayer.isha,
        "Tahajjud Prayer": prayer.tahajjud,
    }

    return prayer_map.get(name)

def build_prayer_event_body(prayer_google_event):
    start_time = get_prayer_start_time(
        prayer_google_event
    )

    if start_time is None:
        return None

    prayer = prayer_google_event.prayer

    end_time = start_time + timedelta(
        minutes=30
    )

    return {
        "summary": prayer_google_event.prayer_name,

        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": prayer.timezone,
        },

        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": prayer.timezone,
        },
    }
    
def sync_one_prayer_event(prayer_google_event, service):
    print(
        "Building Google event body for:",
        prayer_google_event.prayer_name
    )
    
    event_body = build_prayer_event_body(
        prayer_google_event
    )
    
    print(
        "Google event body:",
        event_body
    )


    if event_body is None:
        print(
            "✗ Event body is None"
        )
        return None

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()
    
    print(
        "Google created event:",
        created_event.get("id")
    )
    
    start_time = get_prayer_start_time(
        prayer_google_event
    )

    prayer_google_event.google_event_id = (
        created_event["id"]
    )

    prayer_google_event.needs_google_sync = False
    prayer_google_event.last_synced_start_time = start_time

    prayer_google_event.save(
        update_fields=[
            "google_event_id",
            "needs_google_sync",
            "last_synced_start_time",
        ]
    )
    
    print(
        "✓ Saved Google event ID to database"
    )

    return created_event

def update_prayer_google_event(
    prayer_google_event,
    service
):
    if not prayer_google_event.google_event_id:
        raise ValueError(
            "Prayer event has no Google event ID."
        )

    event_body = build_prayer_event_body(
        prayer_google_event
    )

    if event_body is None:
        return None

    updated_event = service.events().update(
        calendarId="primary",
        eventId=prayer_google_event.google_event_id,
        body=event_body
    ).execute()
    
    start_time = get_prayer_start_time(
        prayer_google_event
    )

    prayer_google_event.needs_google_sync = False
    prayer_google_event.last_synced_start_time = start_time

    prayer_google_event.save(
        update_fields=[
            "needs_google_sync",
            "last_synced_start_time"
        ]
    )

    return updated_event

def sync_user_prayers(user, batch_size=20):
    service = get_google_calendar_service(user)
    
    total_synced = 0
    
    print(
        "\nFinding prayer events needing sync..."
    )
    
    while True:
        prayer_events = PrayerGoogleEvent.objects.filter(
            user=user,
            needs_google_sync=True,
            pending_google_delete=False
        )[:batch_size]
    
        print(
            "Prayer events found:",
            len(prayer_events)
        )
        
        if not prayer_events:
            print("no prayer left to sync")
            break
        
        print(
            "Total waiting:",
            PrayerGoogleEvent.objects.filter(
                user=user,
                needs_google_sync=True,
                pending_google_delete=False
            ).count()
        )

        print(
            "Batch being processed:",
            len(prayer_events)
        )

        for prayer_event in prayer_events:
            print(
                "\nSyncing prayer:",
                prayer_event.prayer_name
            )

            print(
                "Date:",
                prayer_event.prayer.date
            )

            print(
                "Google event ID:",
                prayer_event.google_event_id
            )
            try:
                if prayer_event.google_event_id:
                    
                    print(
                        "Updating existing Google event..."
                    )

                    update_prayer_google_event(
                        prayer_event,
                        service
                    )
                else:
                    
                    print(
                        "Creating new Google event..."
                    )
                    
                    sync_one_prayer_event(
                        prayer_event,
                        service
                    )

                tm.sleep(0.1)
                print(
                    "✓ Prayer synced:",
                    prayer_event.prayer_name
                )

            except HttpError as e:
                error_text = str(e)

                if (
                    e.resp.status in [403, 429]
                    and "rateLimitExceeded" in error_text
                ):
                    print(
                        f"Rate limit hit for "
                        f"{prayer_event.prayer_name} "
                        f"on {prayer_event.prayer.date}. "
                        f"Waiting 5 seconds..."
                    )

                    tm.sleep(5)
                    try:
                        if prayer_event.google_event_id:
                            update_google_event(
                                prayer_event,
                                service
                            )
                        else:
                            sync_one_prayer_event(
                                prayer_event,
                                service
                            )

                    except HttpError as retry_error:
                        print(
                            "Retry failed:",
                            prayer_event.prayer_name,
                            retry_error
                        )

                else:
                    print(
                        "Failed:",
                        prayer_event.prayer_name,
                        prayer_event.prayer.date,
                        e
                    )
                
    
def mark_changed_user_events(user):
    events = UserEvent.objects.filter(
        user=user
    )

    for user_event in events:
        current_hash = get_user_event_hash(
            user_event
        )

        if (
            user_event.last_synced_hash
            != current_hash
        ):
            if not user_event.needs_google_sync:
                user_event.needs_google_sync = True

                user_event.save(
                    update_fields=[
                        "needs_google_sync"
                    ]
                )
                
                
def delete_google_event(user_event, service):
    if user_event.google_event_id:
        try:
            service.events().delete(
                calendarId="primary",
                eventId=user_event.google_event_id
            ).execute()

        except HttpError as e:
            # If Google says it is already gone,
            # we can still safely delete our local row.
            if e.resp.status != 404:
                raise

    user_event.delete()
    
def delete_google_prayer_event(
    prayer_event,
    service
):
    if prayer_event.google_event_id:
        try:
            service.events().delete(
                calendarId="primary",
                eventId=prayer_event.google_event_id
            ).execute()

        except HttpError as e:
            if e.resp.status != 404:
                raise

    prayer_event.delete()
    
    
def sync_deleted_prayer_events(
    user,
    batch_size=20
):
    service = get_google_calendar_service(
        user
    )
    
    total = 0
    
    while True:

        prayer_events = (
            PrayerGoogleEvent.objects.filter(
                user=user,
                pending_google_delete=True
            )[:batch_size]
        )
        
        if not prayer_events:
            break
        
        print(
            f"Deleting batch of "
            f"{len(prayer_events)} prayer events..."
        )

        for prayer_event in prayer_events:
            try:
                print(
                    "Deleting prayer:",
                    prayer_event.prayer_name,
                    prayer_event.prayer.date
                )
                
                delete_google_prayer_event(
                    prayer_event,
                    service
                )

                total += 1
                
                tm.sleep(0.1)

            except HttpError as e:
                print(
                    "Failed to delete prayer:",
                    prayer_event.prayer_name,
                    prayer_event.prayer.date,
                    e
                )
        
    print(
        "Total prayer events deleted:",
        total
    )
    

def sync_deleted_user_events(user, batch_size=20):
    service = get_google_calendar_service(user)
    total = 0
    
    while True:

        events = UserEvent.objects.filter(
            user=user,
            pending_google_delete=True
        )[:batch_size]
        
        if not events:
            break
        
        print(
            f"Deleting batch of "
            f"{len(events)} user events..."
        )

        for user_event in events:
            try:
                print(
                    "Deleting:",
                    user_event.occurrence.event.name,
                    user_event.occurrence.gregorian_date
                )
                
                delete_google_event(
                    user_event,
                    service
                )

                total += 1
                tm.sleep(0.1)

            except HttpError as e:
                print(
                    "Failed to delete:",
                    user_event.occurrence.event.name,
                    e
                )
    print(
        "Total user events deleted:",
        total
    )
            
def sync_everything_for_user(user, event_batch_size=20, prayer_batch_size=20):
    
    print("\n--- GOOGLE SYNC START ---")

    print(
        "Deleting old user events..."
    )
    
    sync_deleted_user_events(
        user,
        batch_size=event_batch_size
    )
    print(
        "Deleting old prayer events..."
    )
    
    sync_deleted_prayer_events(
        user,
        batch_size=prayer_batch_size
    )
    
    print(
        "Syncing normal user events..."
    )

    sync_user_calendar(
        user,
        batch_size=event_batch_size
    )
    
    print(
        "Syncing prayer events..."
    )


    sync_user_prayers(
        user,
        batch_size=prayer_batch_size
    )
    
    print(
        "--- GOOGLE SYNC END ---\n"
    )