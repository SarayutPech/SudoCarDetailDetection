from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('getLicensePlate/', GetLicensePlate.as_view()),
    path('loadImage/', LoadImageSet.as_view()),
    path('resizeImage/', resizeImageSet.as_view()),
]
