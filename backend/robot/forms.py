from django import forms
from .models import Robot

class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['name', 'status']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700 bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        #     'location': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700 bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        # }