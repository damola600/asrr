from django.db import models
from django.contrib.auth.models import User
from hijr_cal.models import EventOccurrence
from prayers.models import Prayer


# Create your models here.
class UserEvent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="scheduled_events"
    )

    occurrence = models.ForeignKey(
        EventOccurrence,
        on_delete=models.CASCADE,
        related_name="user_schedules"
    )
    

    start_time = models.DateTimeField(
        null=True,
        blank=True
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    reminder_at = models.DateTimeField(
        null=True,
        blank=True
    )

    all_day = models.BooleanField(default=False)
    
    google_event_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    synced_to_google = models.BooleanField(
        default=False
    )
    
    last_synced_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    
    pending_google_delete = models.BooleanField(
        default=False
    )
    
    needs_google_sync = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "occurrence"],
                name="unique_user_event_occurrence"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.occurrence.event.name} - "
            f"{self.occurrence.gregorian_date}")


class GoogleCalendarConnection(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="google_calendar_connection"
    )

    access_token = models.TextField(
        null=True,
        blank=True
    )

    refresh_token = models.TextField(
        null=True,
        blank=True
    )

    token_uri = models.CharField(
        max_length=255,
        default="https://oauth2.googleapis.com/token"
    )

    scopes = models.TextField(
        blank=True
    )

    token_expiry = models.DateTimeField(
        null=True,
        blank=True
    )

    connected = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - Google Calendar"
    

class PrayerGoogleEvent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    prayer = models.ForeignKey(
        Prayer,
        on_delete=models.CASCADE
    )

    prayer_name = models.CharField(
        max_length=50
    )

    google_event_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    
    last_synced_start_time = models.DateTimeField(
        null=True,
        blank=True
    )
    
    last_synced_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    
    pending_google_delete = models.BooleanField(default=False)

    needs_google_sync = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "prayer",
                    "prayer_name"
                ],
                name="unique_user_prayer_google_event"
            )
        ]