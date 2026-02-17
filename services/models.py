from django.db import models

# Create your models here.
from django.db import models
from professionals.models import Professional

class Service(models.Model):
    name = models.CharField(max_length=120)
    price_cents = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(default=60)
    professionals = models.ManyToManyField(Professional, related_name="services")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
