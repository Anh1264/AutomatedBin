from django.urls import path
from . import views

urlpatterns=[
    path('images/', views.OttoMixinView.as_view(), name='images'),
    path('images/<str:image_id>/', views.OttoMixinView.as_view(), name='images_detail'),
]