
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from hijr_cal.models import Hijr_cal, Events, EventOccurrence
from hijr_cal.services import (
    save_hijri_cal,
    load_events_from_json,
    create_hijri_date_occurrence,
    create_hijri_range_occurrences,
    create_every_hijri_month_occurrences,
    create_weekday_occurrences,
    create_daily_occurrences,
    create_hijri_month_occurrences,
)


class Command(BaseCommand):
    help = "Initialize Islamic calendar definitions and occurrences."

    def handle(self, *args, **options):
        today = date.today()

        base_dir = Path(__file__).resolve().parents[2]

        holiday_file = base_dir / "data" / "holiday_events.json"
        sunnah_file = base_dir / "data" / "sunnah_acts.json"

        self.stdout.write("Initializing ASRR Islamic calendar...")

        # Load event definitions first.
        with transaction.atomic():
            for file_path in (holiday_file, sunnah_file):
                if not file_path.is_file():
                    raise FileNotFoundError(
                        f"Missing calendar definitions: {file_path}"
                    )

                load_events_from_json(file_path)

        # Generate Gregorian/Hijri dates for the current year.
        # Include January onward so the calendar is complete.
        save_hijri_cal(1, today.year)

        # Generate occurrences using existing services.
        with transaction.atomic():
            create_hijri_date_occurrence()
            create_hijri_range_occurrences()
            create_every_hijri_month_occurrences()
            create_weekday_occurrences()
            create_daily_occurrences()
            create_hijri_month_occurrences()

        self.stdout.write(
            self.style.SUCCESS(
                "Calendar initialization completed.\n"
                f"Hijri dates: {Hijr_cal.objects.count()}\n"
                f"Definitions: {Events.objects.count()}\n"
                f"Occurrences: {EventOccurrence.objects.count()}"
            )
        )
