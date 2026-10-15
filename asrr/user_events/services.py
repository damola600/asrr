from members.services import build_user_schedule
from .prayer_services import build_user_prayer_events
from .google_cal import sync_everything_for_user, mark_changed_user_events
from user_events.models import UserEvent

def refresh_user_calendar(user,event_batch_size=20,prayer_batch_size=20):
    
    print("\n==============================")
    print("REFRESH USER CALENDAR")
    print("==============================")
    
    if user is None:
        raise ValueError("A valid user is required.")
    
    print(
        "User:",
        user.email
    )


    print(
        "\n1. Building normal user schedule..."
    )
    
    build_user_schedule(user)
    
    print("\n=== USER EVENT DEBUG ===")

    print(
        "Total UserEvents:",
        UserEvent.objects.filter(
            user=user
        ).count()
    )

    print(
        "UserEvents needing sync:",
        UserEvent.objects.filter(
            user=user,
            needs_google_sync=True,
            pending_google_delete=False
        ).count()
    )

    print(
        "UserEvents pending delete:",
        UserEvent.objects.filter(
            user=user,
            pending_google_delete=True
        ).count()
    )

    print("========================\n")
    
    print(
        "✓ User schedule built"
    )


    print(
        "\n2. Building prayer events..."
    )

    build_user_prayer_events(user)
    
    print(
        "✓ Prayer events built"
    )


    print(
        "\n3. Checking changed events..."
    )

    mark_changed_user_events(user)
    
    print(
        "✓ Changed events marked"
    )

    
    connection = getattr(
        user,
        "google_calendar_connection",
        None
    )

    if (connection is None or not connection.connected):
        print(
            "✗ No Google Calendar connection"
        )
        return
    
    print(
        "Google connected:",
        connection.connected
    )


    if not connection.connected:

        print(
            "✗ Google Calendar is not active"
        )

        return


    print(
        "\n4. Starting Google Calendar sync..."
    )


    sync_everything_for_user(user,event_batch_size=event_batch_size,prayer_batch_size=prayer_batch_size)
    
    print(
        "✓ Google sync finished"
    )

    print(
        "==============================\n"
    )