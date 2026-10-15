import requests
import json
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder

load_dotenv()
URL = "https://ummahapi.com/api/prayer-times/month"

def get_lat_long(
    city: str,
    country: str
) -> dict:
    geoloc = Nominatim(
        user_agent="city_geocoder"
    )

    try:
        loc = geoloc.geocode(
            f"{city}, {country}"
        )

        if loc is None:
            raise ValueError(
                "Invalid city or country."
            )

        tf = TimezoneFinder()

        timezone_name = (
            tf.timezone_at(
                lng=loc.longitude,
                lat=loc.latitude
            )
        )

        if timezone_name is None:
            raise ValueError(
                "Could not determine timezone."
            )

        return {
            "lat": loc.latitude,
            "long": loc.longitude,
            "timezone": timezone_name,
        }

    except ValueError:
        raise

    except Exception as e:
        raise ValueError(
            "Unable to locate city/country."
        ) from e
    
def calc_tahajjud_time(maghrib, fajr):
    maghrib_dt = datetime.strptime(maghrib, "%Y-%m-%d %H:%M")
    fajr_dt = datetime.strptime(fajr, "%Y-%m-%d %H:%M")
    
    fajr_dt += timedelta(days=1)
    
    night_duration = fajr_dt - maghrib_dt
    one_third = night_duration / 3
    tahajjud_start = fajr_dt - one_third
    
    return tahajjud_start.strftime('%I:%M')

def calc_duha_time(sunrise):
    sunrise_time = datetime.strptime(sunrise, "%H:%M")
    after_sunrise = sunrise_time + timedelta(minutes=15)
    return after_sunrise.strftime("%H:%M")

def get_prayer_data(city: str, madhab: str, month: str, year:str, country: str = "Canada")-> list[dict]:
    coord = get_lat_long(city, country)
    params = {
        "latitude": coord['lat'],
        "longitude": coord['long'],
        "method": "NorthAmerica",
        "month": month,
        "year": year,
        "madhab": madhab,
        "timezonestring": "UTC",
        "latitudeAdjustmentMethod": 1,
        "calendarMethod": "UAQ",
        "iso8601": "false"
    }

    headers = {
        'X-API-Key':os.getenv('UMMAH_API_KEY')
    }

    res = requests.get(URL, params=params, headers=headers, timeout=30)
    
    res.raise_for_status()

    data = res.json()

    days = data["data"]["days"]
    prayer_data = []

    for day in days:
        date = day["date"]
        prayers = day["prayer_times"]
        prayer = {
            "Date": date,
            "Timezone": coord["timezone"],
            "Fajr": prayers["fajr"],
            "Duha": calc_duha_time(prayers["sunrise"]),
            "Sunrise": prayers["sunrise"],
            "Dhuhr": prayers["dhuhr"],
            "Asr": prayers["asr"],
            "Maghrib": prayers["maghrib"],
            "Isha": prayers["isha"],
            "Tahajjud": calc_tahajjud_time(f'{date} {prayers["maghrib"]}', f'{date} {prayers["fajr"]}')
        }
        prayer_data.append(prayer)
    
    return prayer_data


