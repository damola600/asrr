from celery import shared_task
from django.contrib.auth.models import User
from prayers.services import save_prayer_data
from user_events.services import refresh_user_calendar
from datetime import date



@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_user_calendar_task(self, user_id):
    try:
        user = User.objects.select_related(
                'profile', 'sunnah_pref', 'google_calendar_connection'
            ).get(
                id=user_id
            )
        
        member = user.profile
        today = date.today()
        
        save_prayer_data(
            city=member.city,
            country=member.country,
            madhab=member.madhab,
            st_month=today.month,
            year=today.year
        )
        
        refresh_user_calendar(user)
        
        return{
            'success': True,
            'user_id': user_id,
        }
    
    except User.DoesNotExist:
        return {
            'success': False,
            'error': 'User not found',
        }
        
    except Exception as exc:
        raise self.retry(exc=exc)