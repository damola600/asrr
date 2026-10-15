from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils import timezone

from .models import Prayer
from .helpers import get_prayer_data

def format_dt(date_str, time_str, timezone_name):
    dt = datetime.strptime(f'{date_str} {time_str}', "%Y-%m-%d %H:%M")
    
    return dt.replace(
        tzinfo=ZoneInfo(timezone_name)
    )

def save_prayer_data(city, madhab, st_month, year, country='Canada'):
    
    
    for mth in range(st_month, 13):
        prayer_data = get_prayer_data(city, madhab, mth, year, country)
    
        for day in prayer_data:
            date = day['Date']
            timezone = day['Timezone']
            
            Prayer.objects.update_or_create(
                date=date,
                city=city,
                country=country,
                madhab=madhab,

                defaults={
                    "timezone": timezone,

                    "fajr": format_dt(
                        date,
                        day["Fajr"],
                        timezone
                    ),

                    "sunrise": format_dt(
                        date,
                        day["Sunrise"],
                        timezone
                    ),

                    "duha": format_dt(
                        date,
                        day["Duha"],
                        timezone
                    ),

                    "dhuhr": format_dt(
                        date,
                        day["Dhuhr"],
                        timezone
                    ),

                    "asr": format_dt(
                        date,
                        day["Asr"],
                        timezone
                    ),

                    "maghrib": format_dt(
                        date,
                        day["Maghrib"],
                        timezone
                    ),

                    "isha": format_dt(
                        date,
                        day["Isha"],
                        timezone
                    ),

                    "tahajjud": format_dt(
                        date,
                        day["Tahajjud"],
                        timezone
                    ),
                }
            )