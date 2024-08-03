from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Robot
from django.db import transaction

# notify the changes on status, including previous and current status
def notify_mcu(robot_id, status):
    """
    Notify the MCU of the robot's status change.
    
    Args:
        robot_id (int): The ID of the robot.
        status (bool): The new status of the robot (True for on, False for off).
    """
    print("Robot ID:", robot_id, "Robot Status:", status)

@receiver(pre_save, sender=Robot)
def capture_previous_status(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(pk=instance.pk)
        instance._previous_status = previous_instance.status
        return instance._previous_status
    except sender.DoesNotExist:
        # This is a new instance, so there's no previous status
        instance._previous_status = None

@receiver(post_save, sender=Robot)
def notify_mcu_on_status_change(sender, instance, **kwargs):
    previous_status = getattr(instance, '_previous_status', None)
    current_status = instance.status

    print(previous_status, current_status)

    if previous_status != current_status:
        notify_mcu(instance.robot_id, current_status)