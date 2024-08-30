from otto.utils.background_wrapper import run_in_background
from robot.models import Robot
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from otto.models import OttoImage, OttoInference
from .save_gg_images import get_drive_link

@run_in_background
def save_image_data(b64_image_data,  robot_id, inference_response,):
    try:
        robot_ins = Robot.objects.get(id=robot_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Robot not found"}, status=404)

    with transaction.atomic():  # Ensure data consistency
        try:
            otto_inference = OttoInference.objects.create(
                detected_type=inference_response.detected_type,
                confidence=inference_response.confidence,
                processing_time=inference_response.processing_time
            )
            #file name as inference id
            #folder name as robot id
            inference_id = otto_inference.id
            print('robot_id:', robot_id)
            print('inference_id:', inference_id)
            url = get_drive_link(b64_image_data, file_name=inference_id, folder_name=robot_id)
            print('Drive Link:' ,url)

        except Exception as e:
            return JsonResponse({"error": f"Failed to create OttoInference or OttoImage: {e}"}, status=500)
            
        

    try:
        otto_image = OttoImage.objects.create(
        url=url,
        inference=otto_inference,  
        image_data=b64_image_data,
        robot=robot_ins,
    )

    except Exception as e:
        return JsonResponse(
            {"error":f"Failed to create OttoImage instance: {e}"}, status=500
        )
        
    print("Inference:",otto_inference)
    print("Robot instance:", robot_ins)
    print("Image:",otto_image)