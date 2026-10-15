from django.db import models

# Create your models here.
class Hijr_cal(models.Model):
    gregorian_date = models.DateField(unique=True)
    
    hijri_day = models.PositiveSmallIntegerField()
    hijri_month = models.PositiveSmallIntegerField()
    hijri_year = models.PositiveIntegerField()

    hijri_month_name = models.CharField(
        max_length=50
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.gregorian_date} -> "
            f"{self.hijri_day} "
            f"{self.hijri_month_name} "
            f"{self.hijri_year}"
        )

# Create your models here.
class Events(models.Model):
    EVENT_TYPES = [
        ('HOLIDAY', 'Islamic Holiday'),
        ('FAST', 'Sunnah Fast'),
        ('PRAYER', 'Sunnah Prayer'),
        ('SUNNAH', 'Other Sunnah Act'),
    ]
    
    TIME_TYPES = [
        ('ALL_DAY', 'All Day'),
        ('PRAYER_RELATIVE', 'Based on Prayer Time'),
        ('TAHAJJUD', 'Calculated Last Third of Night')
    ]
    
    PRAYER_REFERENCES = [
    ("FAJR", "Fajr"),
    ("SUNRISE", "Sunrise"),
    ("DHUHR", "Dhuhr"),
    ("ASR", "Asr"),
    ("MAGHRIB", "Maghrib"),
    ("ISHA", "Isha"),
]
    
    DATE_TYPES = [
        ("HIJRI_DATE", "Specific Hijri Date"),
        ("HIJRI_RANGE", "Hijri Date Range"),
        ("EVERY_HIJRI_MONTH", "Every Hijri Month"),
        ("WEEKDAY", "Weekday"),
        ("PRAYER_TIME", "Calculated From Prayer Time"),
        ('DAILY', 'Every Day'),
        ("HIJRI_MONTH", "Hijri Month"),
    ]
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date_type = models.CharField(max_length=30, choices=DATE_TYPES)
    hijri_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    hijri_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    hijri_end_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    weekday = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    
    time_type = models.CharField(
        max_length=30,
        choices=TIME_TYPES,
        default="ALL_DAY"
    )

    reference_prayer = models.CharField(
        max_length=20,
        choices=PRAYER_REFERENCES,
        null=True,
        blank=True
    )

    offset_minutes = models.IntegerField(default=0)

    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    moon_sighting_sensitive = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name
    


class EventOccurrence(models.Model):
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        related_name="occurrences"
    )

    hijri_date = models.ForeignKey(
        Hijr_cal,
        on_delete=models.CASCADE,
        related_name="event_occurrences",
        null=True,
        blank=True
    )
    
    gregorian_date = models.DateField()
    
    all_day = models.BooleanField(default=False)

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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "gregorian_date"],
                name="unique_act_occurrence"
            )
        ]

    def __str__(self):
        return f"{self.event.name} - {self.gregorian_date}"

