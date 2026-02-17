from django.db import models

# Create your models here.
from django.db import models

class Professional(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    whatsapp_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
