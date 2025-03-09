from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
router.registry(r'user', UserProfileAPIView, basename='user_list')


urlpatterns = [
    path('', include(router.urls))
]
