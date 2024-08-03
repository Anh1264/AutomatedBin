from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import mixins, generics
from .models import Robot
from .serializers import RobotSerializer

# Create your views here.
class RobotMixinView(
    generics.GenericAPIView, 
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    ):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        robot_id = kwargs.get('id')
        if robot_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
