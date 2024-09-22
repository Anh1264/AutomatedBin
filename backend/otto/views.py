# Create your views here.
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import OttoImageSerializer
from .models import OttoImage
from .services.AI_infer import return_infer_response
from .tasks.background_tasks import serialize_otto_image_task, save_image_data_task
from celery import chain

class OttoMixinView(
    generics.GenericAPIView, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    ):
    queryset = OttoImage.objects.all()
    serializer_class = OttoImageSerializer
    lookup_field = "image_id"

    def get(self, request, *args, **kwargs):
        picture_id = kwargs.get('image_id')
        if picture_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(*args, **kwargs)
        try:
            robot_id = request.data.get('robot_id')
            b64_image_data = request.data.get('image_data')
            print('robot_id:', robot_id)

            inference_response = return_infer_response(b64_image_data)
            print(inference_response)
            print("Celery tasks about to initiate")
            # Get the fully qualified serializer class name
            serializer_class_name = self.get_serializer_class().__module__ + '.' + self.get_serializer_class().__name__


            # chain the two task together
            result = chain(
                serialize_otto_image_task.s(
                    robot_id, 
                    b64_image_data, 
                    inference_response, 
                    serializer_class_name,
                ),
                save_image_data_task.s(b64_image_data, robot_id, inference_response)
            )()
            # Return the serialized inference response
            return Response({
                'inference_response': inference_response
            })
        except ValidationError as e:
            return Response({"errors": e.detail})

    def perform_create(self, serializer):
        return serializer.save()
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)