import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_hijr_cal(month, yr):
    cal_url = f"https://api.aladhan.com/v1/gToHCalendar/{month}/{yr}"
    
    params = {
        "calendarMethod":"UAQ"
    }
    
    res = requests.get(cal_url, params=params, timeout=30)
    
    data = res.json()['data']
    
    hijri_data = []

    for day in data:
        hijri = day["hijri"]
        gregorian = day["gregorian"]

        calendar_day = {
            "gregorian_date": gregorian["date"],
            "hijri_day": hijri["day"],
            "hijri_month": hijri["month"]["number"],
            "hijri_month_name": hijri["month"]["en"],
            "hijri_year": hijri["year"]
        }

        hijri_data.append(calendar_day)
    
    return hijri_data
    



def get_islamic_events():
    url = 'https://ummahapi.com/api/islamic-events'
    
    header = {
        'X-API-Key':os.getenv('UMMAH_API_KEY')
    }
    
    res = requests.get(url, headers=header, timeout=30)
    
    res.raise_for_status()

    return res.json()