from hijr_cal.models import EventOccurrence
from user_events.models import UserEvent
from datetime import timedelta
from prayers.models import Prayer

SUNNAH_PREFERENCE_MAP = {
    "monday-sunnah-fast": "monday_fast",
    "thursday-sunnah-fast": "thursday_fast",
    "white-days-fast": "white_days_fast",
    "arafah-fast": "arafah_fast",
    "ashura-fast": "ashura_fast",
    "first-nine-dhul-hijjah-fast": "first_nine_dhul_hijjah",
    "six-days-of-shawwal": "six_days_shawwal",

    "surah-al-kahf": "surah_kahf_fri",
    
    "friday-dua": "friday_dua",
    "friday-preparation": "friday_preparation",

    "arafah-dua": "arafah_dua",
    "surah-al-mulk": "surah_mulk_daily",

    "morning-adhkar": "morning_adhkar",
    "evening-adhkar": "evening_adhkar",

    "tahajjud": "tahajjud",
    "duha": "duha",
}


def is_sunnah_event_enabled(user, event):
    if not hasattr(user, "sunnah_pref"):
        print(
            f"SKIP {event.slug}: "
            "no sunnah_pref"
        )
        return False

    sunnah = user.sunnah_pref

    if not sunnah.sunnah_enabled:
        print(
            f"SKIP {event.slug}: "
            "master Sunnah disabled"
        )
        return False

    preference_field = SUNNAH_PREFERENCE_MAP.get(
        event.slug
    )

    if preference_field is None:
        print(
            f"SKIP {event.slug}: "
            "slug not in SUNNAH_PREFERENCE_MAP"
        )
        return False

    enabled =  getattr(
        sunnah,
        preference_field,
        False
    )
    
    print(
        f"{event.slug} -> "
        f"{preference_field} -> "
        f"{enabled}"
    )

    return enabled


def get_user_prayer(user, date):
    member = user.profile

    return Prayer.objects.filter(
        date=date,
        city=member.city,
        country=member.country,
        madhab=member.madhab,
    ).first()

def create_timed_user_events(user):
    occurrences = (
        EventOccurrence.objects.filter(
            all_day=False,
            event__time_type=
                "PRAYER_RELATIVE"
        )
    )

    for occurrence in occurrences:
        event = occurrence.event

        if event.event_type in [
            "FAST",
            "PRAYER",
            "SUNNAH",
        ]:
            if not is_sunnah_event_enabled(
                user,
                event
            ):
                UserEvent.objects.filter(
                    user=user,
                    occurrence=occurrence
                ).update(
                    pending_google_delete=True,
                    needs_google_sync=False,
                )
                continue

        prayer = get_user_prayer(
            user,
            occurrence.gregorian_date
        )

        if prayer is None:
            continue

        prayer_times = {
            "FAJR": prayer.fajr,
            "SUNRISE": prayer.sunrise,
            "DHUHR": prayer.dhuhr,
            "ASR": prayer.asr,
            "MAGHRIB": prayer.maghrib,
            "ISHA": prayer.isha,
        }

        reference_time = (
            prayer_times.get(
                event.reference_prayer
            )
        )

        if reference_time is None:
            continue

        start_time = (
            reference_time
            + timedelta(
                minutes=event.offset_minutes
            )
        )

        end_time = None

        if event.duration_minutes:
            end_time = (
                start_time
                + timedelta(
                    minutes=
                        event.duration_minutes
                )
            )

        UserEvent.objects.update_or_create(
            user=user,
            occurrence=occurrence,

            defaults={
                "all_day": False,
                "start_time": start_time,
                "end_time": end_time,
                "reminder_at": None,
                "pending_google_delete": False,
                "needs_google_sync": True,
            }
        )


def create_all_day_user_events(user):
    occurrences = (
        EventOccurrence.objects.filter(
            all_day=True
        )
    )

    for occurrence in occurrences:
        event = occurrence.event

        if event.event_type in [
            "FAST",
            "PRAYER",
            "SUNNAH",
        ]:
            enabled = (
                is_sunnah_event_enabled(
                    user,
                    event
                )
            )

            if not enabled:
                UserEvent.objects.filter(
                    user=user,
                    occurrence=occurrence
                ).update(
                    pending_google_delete=True,
                    needs_google_sync=False,
                )

                continue

        UserEvent.objects.update_or_create(
            user=user,
            occurrence=occurrence,

            defaults={
                "all_day": True,
                "start_time": None,
                "end_time": None,
                "reminder_at": None,
                "pending_google_delete":
                    False,
                "needs_google_sync": True,
            }
        )


def add_fast_reminders(user):
    fast_events = UserEvent.objects.filter(
        user=user,
        occurrence__event__event_type="FAST",
        all_day=True,
        pending_google_delete=False
    )

    for user_event in fast_events:
        event = user_event.occurrence.event
        

        if not is_sunnah_event_enabled(
            user,
            event
        ):
            continue

        fast_date = (
            user_event
            .occurrence
            .gregorian_date
        )

        previous_date = (
            fast_date
            - timedelta(days=1)
        )

        previous_prayer = (
            get_user_prayer(
                user,
                previous_date
            )
        )

        if previous_prayer is None:
            continue

        reminder_time = (
            previous_prayer.maghrib
            + timedelta(minutes=15)
        )

        user_event.reminder_at = (
            reminder_time
        )

        user_event.save(
            update_fields=[
                "reminder_at"
            ]
        )


def build_user_schedule(user):
    
    print("\n in build user schedule")
    print("User:", user.email)
    
    if not hasattr(user, "sunnah_pref"):
        print("✗ User has no Sunnah preferences")
        return

    sunnah = user.sunnah_pref

    print(
        "Master Sunnah:",
        sunnah.sunnah_enabled
    )

    print(
        "Preferences:",
        sunnah.__dict__
    )
    
    
    if user is None:
        raise ValueError(
            "A valid user is required."
        )

    create_all_day_user_events(user)
    
    print(
        "UserEvents after all-day:",
        UserEvent.objects.filter(
            user=user
        ).count()
    )

    print("\nCreating timed events...")
    
    create_timed_user_events(user)
    
    print(
        "UserEvents after timed:",
        UserEvent.objects.filter(
            user=user
        ).count()
    )

    print("\nAdding fast reminders...")
    
    add_fast_reminders(user)
    
    print(
        "FINAL UserEvents:",
        UserEvent.objects.filter(
            user=user
        ).count()
    )

    print("================================\n")