from django.db import models


# Create your models here.
class Prayer(models.Model):
    
    date = models.DateField()
    
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    madhab = models.CharField(max_length=20, default="shafi")
    
    fajr = models.DateTimeField()
    sunrise = models.DateTimeField()
    duha = models.DateTimeField(
        null=True,
        blank=True
    )
    dhuhr = models.DateTimeField()
    asr = models.DateTimeField()
    maghrib = models.DateTimeField()
    isha = models.DateTimeField()
    tahajjud = models.DateTimeField(
    null=True,
    blank=True
)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "city", "country", "madhab"],
                name="unique_prayer_time_location_date"
            )
        ]

    def __str__(self):
        return f"{self.city}, {self.country} - {self.madhab} - {self.date}"

