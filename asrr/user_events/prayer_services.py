from prayers.models import Prayer
from user_events.models import PrayerGoogleEvent


PRAYER_FIELDS = [
    ("Fajr", "fajr"),
    ("Dhuhr", "dhuhr"),
    ("Asr", "asr"),
    ("Maghrib", "maghrib"),
    ("Isha", "isha"),
]


def build_user_prayer_events(user):
    if user is None:
        raise ValueError("A valid user is required.")

    member = user.profile

    # ==========================================
    # PRAYER CALENDAR DISABLED
    # ==========================================

    if not member.prayer_enabled:

        print("Prayer calendar disabled.")

        updated = PrayerGoogleEvent.objects.filter(
            user=user
        ).update(
            pending_google_delete=True,
            needs_google_sync=False
        )

        print(
            f"Marked {updated} prayer events "
            f"for Google deletion."
        )

        return

    print("Prayer calendar enabled.")

    # ==========================================
    # MARK OLD LOCATION / MADHAB FOR DELETION
    # ==========================================

    old_events = PrayerGoogleEvent.objects.filter(
        user=user
    ).exclude(
        prayer__city=member.city,
        prayer__country=member.country,
        prayer__madhab=member.madhab
    )

    old_count = old_events.update(
        pending_google_delete=True,
        needs_google_sync=False
    )

    if old_count:
        print(
            f"Marked {old_count} old-location "
            f"prayer events for deletion."
        )

    # ==========================================
    # GET CURRENT PRAYER DATA
    # ==========================================

    prayers = Prayer.objects.filter(
        city=member.city,
        country=member.country,
        madhab=member.madhab
    )

    # ==========================================
    # CHECK TAHAJJUD PREFERENCE
    # ==========================================

    tahajjud_enabled = (
        hasattr(user, "sunnah_pref")
        and user.sunnah_pref.sunnah_enabled
        and user.sunnah_pref.tahajjud
    )

    # Tahajjud disabled → remove existing
    # Tahajjud Google events.
    if not tahajjud_enabled:

        tahajjud_deleted = (
            PrayerGoogleEvent.objects.filter(
                user=user,
                prayer_name="Tahajjud Prayer"
            ).update(
                pending_google_delete=True,
                needs_google_sync=False
            )
        )

        if tahajjud_deleted:
            print(
                f"Marked {tahajjud_deleted} "
                f"Tahajjud events for deletion."
            )

    # ==========================================
    # PRAYERS THAT SHOULD CURRENTLY EXIST
    # ==========================================

    prayer_fields = PRAYER_FIELDS.copy()

    if tahajjud_enabled:
        prayer_fields.append(
            ("Tahajjud Prayer", "tahajjud")
        )

    # ==========================================
    # CREATE / RESTORE / UPDATE EVENTS
    # ==========================================

    for prayer in prayers:

        for prayer_name, field_name in prayer_fields:

            start_time = getattr(
                prayer,
                field_name
            )

            if start_time is None:
                continue

            prayer_event, created = (
                PrayerGoogleEvent.objects.get_or_create(
                    user=user,
                    prayer=prayer,
                    prayer_name=prayer_name,
                    defaults={
                        "needs_google_sync": True,
                        "pending_google_delete": False
                    }
                )
            )

            # ------------------------------
            # NEW EVENT
            # ------------------------------

            if created:
                continue

            # ------------------------------
            # RESTORE EVENT
            # ------------------------------

            if prayer_event.pending_google_delete:

                prayer_event.pending_google_delete = False
                prayer_event.needs_google_sync = True

                prayer_event.save(
                    update_fields=[
                        "pending_google_delete",
                        "needs_google_sync"
                    ]
                )

                continue

            # ------------------------------
            # PRAYER TIME CHANGED
            # ------------------------------

            if (
                prayer_event.last_synced_start_time
                != start_time
            ):

                prayer_event.needs_google_sync = True

                prayer_event.save(
                    update_fields=[
                        "needs_google_sync"
                    ]
                )