from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from user_events.models import PrayerGoogleEvent
from user_events.google_cal import (
    get_google_calendar_service,
    delete_google_prayer_event,
)


class Command(BaseCommand):
    help = "Delete all prayer events from Google Calendar and local database"

    def handle(self, *args, **options):

        user = User.objects.first()

        if user is None:
            self.stdout.write(
                self.style.ERROR("No user found.")
            )
            return

        self.stdout.write(
            f"User: {user.email}"
        )

        prayer_events = PrayerGoogleEvent.objects.filter(
            user=user
        )

        total = prayer_events.count()

        self.stdout.write(
            f"Prayer events found: {total}"
        )

        if total == 0:
            self.stdout.write(
                self.style.WARNING(
                    "No prayer events to delete."
                )
            )
            return

        # Get Google Calendar service
        try:
            service = get_google_calendar_service(user)

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Could not connect to Google Calendar: {e}"
                )
            )
            return

        deleted = 0
        failed = 0

        while True:

            batch = list(
                PrayerGoogleEvent.objects.filter(
                    user=user
                )[:20]
            )

            if not batch:
                break

            self.stdout.write(
                f"\nDeleting batch of {len(batch)}..."
            )

            for prayer_event in batch:

                try:

                    self.stdout.write(
                        f"Deleting "
                        f"{prayer_event.prayer_name} "
                        f"on {prayer_event.prayer.date}"
                    )

                    delete_google_prayer_event(
                        prayer_event,
                        service
                    )

                    deleted += 1

                except Exception as e:

                    failed += 1

                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed: "
                            f"{prayer_event.prayer_name} "
                            f"{prayer_event.prayer.date}: "
                            f"{e}"
                        )
                    )

                    # Remove it from this cleanup attempt
                    # so we don't create an infinite loop.
                    prayer_event.pending_google_delete = False
                    prayer_event.save(
                        update_fields=[
                            "pending_google_delete"
                        ]
                    )

        self.stdout.write("\n======================")

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted: {deleted}"
            )
        )

        if failed:
            self.stdout.write(
                self.style.WARNING(
                    f"Failed: {failed}"
                )
            )

        remaining = PrayerGoogleEvent.objects.filter(
            user=user
        ).count()

        self.stdout.write(
            f"Remaining local prayer events: {remaining}"
        )

        self.stdout.write("======================")