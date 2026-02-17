from django.db import models

# Create your models here.
from django.db import models
from professionals.models import Professional

class WeeklyAvailability(models.Model):
    WEEKDAYS = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )

    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name="weekly_availabilities"
    )
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.professional.name} - {self.get_weekday_display()}"
