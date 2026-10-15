from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from user_events.global_refresh import refresh_global_data
from user_events.services import refresh_user_calendar


class Command(BaseCommand):
    help = "Refresh Islamic calendar data and sync users"

    def handle(self, *args, **options):
        self.stdout.write(
            "Refreshing global Islamic calendar data..."
        )

        # ----------------------------------------
        # REFRESH GLOBAL DATA
        # ----------------------------------------

        try:
            refresh_global_data()

            self.stdout.write(
                self.style.SUCCESS(
                    "Global data refresh complete."
                )
            )

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(
                    f"Global refresh failed: {e}"
                )
            )

            return

        # ----------------------------------------
        # GET USERS WHO COMPLETED SETUP
        # ----------------------------------------

        users = (
            User.objects
            .select_related(
                "profile",
                "sunnah_pref",
                "google_calendar_connection"
            )
            .filter(
                profile__isnull=False,
                profile__setup_complete=True
            )
        )

        user_count = users.count()

        if user_count == 0:
            self.stdout.write(
                "No completed users found."
            )

            return

        self.stdout.write(
            f"Found {user_count} completed users."
        )

        # ----------------------------------------
        # REFRESH EACH USER
        # ----------------------------------------

        for user in users:
            try:
                self.stdout.write(
                    f"Refreshing {user.username}..."
                )

                refresh_user_calendar(
                    user,
                    event_batch_size=20,
                    prayer_batch_size=20
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Finished {user.username}"
                    )
                )

            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f"Failed {user.username}: {e}"
                    )
                )

        # ----------------------------------------
        # COMPLETE
        # ----------------------------------------

        self.stdout.write(
            self.style.SUCCESS(
                "Calendar refresh finished."
            )
        )