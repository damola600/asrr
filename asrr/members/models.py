from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    MADHAB_CHOICES = [
        ("hanafi", "Hanafi"),
        ("shafi", "Shafi'i"),
        ("maliki", "Maliki"),
        ("hanbali", "Hanbali"),
        ("jaffari", "Ja'fari"),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    email = models.EmailField(unique=True)
    google_cal_email = models.EmailField(unique=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    madhab = models.CharField(max_length=20, choices=MADHAB_CHOICES, default="shafi", blank=True)
    
    setup_complete = models.BooleanField(default=False)
    prayer_enabled = models.BooleanField(default=False)
    # sunnah_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.city}, {self.country}"
    


class Sunnah(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='sunnah_pref'
    )
    
    sunnah_enabled = models.BooleanField(default=False)
    
    # Sunnah salah
    tahajjud = models.BooleanField(default=False)
    duha = models.BooleanField(default=False)
    
    # Sunnah fast
    monday_fast = models.BooleanField(default=False)
    thursday_fast = models.BooleanField(default=False)
    white_days_fast = models.BooleanField(default=False)
    arafah_fast = models.BooleanField(default=False)
    ashura_fast = models.BooleanField(default=False)
    first_nine_dhul_hijjah = models.BooleanField(default=False)
    
    # Others
    surah_kahf_fri = models.BooleanField(default=False)
    morning_adhkar = models.BooleanField(default=False)
    evening_adhkar = models.BooleanField(default=False)
    surah_mulk_daily = models.BooleanField(default=False)
    
    friday_dua = models.BooleanField(default=False)
    friday_preparation = models.BooleanField(default=False)
    arafah_dua = models.BooleanField(default=False)
    six_days_shawwal = models.BooleanField(default=False)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Sunnah Acts: {self.sunnah_enabled}"   



