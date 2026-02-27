from django.db import models

# Create your models here.
from django.db import models
from professionals.models import Professional
from services.models import Service
import uuid
from django.utils import timezone
from datetime import timedelta

class Booking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),             
        ("cancelled", "Cancelled"),
    )

    professional = models.ForeignKey(Professional, on_delete=models.PROTECT, related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="bookings")

    customer_name = models.CharField(max_length=150)
    customer_whatsapp = models.CharField(max_length=20)

    start = models.DateTimeField()
    end = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")
    #função de cancelamento de atendimento
    cancel_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def can_cancel(self):
        limite = self.start - timedelta(hours = 6)
        return timezone.now() <= limite

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} - {self.start:%Y-%m-%d %H:%M}"
