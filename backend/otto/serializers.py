from .models import OttoImage
from rest_framework import serializers

class OttoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OttoImage
        fields = [
            'id',
            'otto_inference',
            'url',
            'image_data',
            'cap_time',
            'robot',
            ]
        
    def create(self, validated_data):
        print("Validated Data:",validated_data)
        instance = OttoImage.objects.create(**validated_data)
        return instance