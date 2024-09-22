from django.db import models
from robot.models import Robot
import uuid


class OttoInference(models.Model):
    detected_type = models.CharField(max_length=100, null=False, blank=True)
    confidence = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    processing_time = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"The image is a: {self.detected_type}"


class OttoImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otto_inference = models.OneToOneField(OttoInference, on_delete=models.SET_NULL, null=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    image_data = models.TextField(null=True, blank=True)
    cap_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # One to many relationship with robot
    robot = models.ForeignKey(Robot, on_delete=models.SET_NULL, null=True) #no more robot

    def __str__(self):
        return f"{self.otto_inference} taken by {self.robot}"

