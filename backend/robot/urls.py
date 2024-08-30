from django.urls import path
from . import views

urlpatterns=[
    path('robots/', views.RobotMixinView.as_view(), name="robots"),
]