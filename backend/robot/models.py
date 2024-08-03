from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Robot(models.Model):
    id = models.AutoField(primary_key=True)
    mac_address = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=False)
    temp = models.FloatField(null=True,blank=True)
    battery = models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.id}.{self.name} - {self.status}"