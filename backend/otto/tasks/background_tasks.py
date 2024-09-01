from robot.models import Robot
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from otto.models import OttoImage, OttoInference
from otto.services.save_gg_images import get_drive_link
from celery import shared_task
from django.utils.module_loading import import_string

@shared_task
def serialize_otto_image_task(robot_id, b64_image_data, inference_response, serializer_class_name):
    serializer_data = {
        'robot': robot_id,
        'image_data': b64_image_data,
        'detected_type': inference_response['detected_type'],
        'confidence': inference_response['confidence'],
        'processing_time': inference_response['processing_time']
    }
    serializer_class = import_string(serializer_class_name)
    try:
        serializer = serializer_class(data=serializer_data)
        if serializer.is_valid():
            otto_image = serializer.save()
            print("Otto Image:", otto_image)
            print(f"Created OttoImage with ID: {otto_image.id}")  # Log success
            return otto_image.id
        else:
            print(f"Serializer errors: {serializer.errors}")  # Log validation errors
            raise Exception("Serializer validation failed")  # Or return an error message
    except Exception as e:
        print(f"Error in serialize_otto_image_task: {e}")  # Log general errors
        raise  # Re-raise the exception to be handled by Celery


@shared_task
def save_image_data_task(otto_image_id, b64_image_data, robot_id, inference_response):
    try:
        print("Arrived otto image id:",otto_image_id)
        robot_ins = Robot.objects.get(id=robot_id)
        otto_image = OttoImage.objects.get(id=otto_image_id)
    except ObjectDoesNotExist:
        return "Error: Robot or OttoImage not found"

    with transaction.atomic():  # Ensure data consistency
        try:
            otto_inference = OttoInference.objects.create(
                detected_type=inference_response['detected_type'],
                confidence=inference_response['confidence'],
                processing_time=inference_response['processing_time']
            )
            #file name as inference id
            #folder name as robot id
            inference_id = otto_inference.id
            print('robot_id:', robot_id)
            print('inference_id:', inference_id)
            url = get_drive_link(b64_image_data, file_name=inference_id, folder_name=robot_id)
            print('Drive Link:' ,url)

        except Exception as e:
            return f"Error: Failed to create OttoInference: {e}"
            
        otto_image.url = url
        otto_image.save()

        
    print("Inference:",otto_inference)
    print("Robot instance:", robot_ins)
    print("Image:",otto_image)
    # Return a success message or relevant data
    return {
        "status": "success",
        "image_id": otto_image.id,
        "url": url
    }
