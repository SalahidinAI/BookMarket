from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')
# router.registry(r'user', UserProfileAPIView, basename='user_list')


urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:book_id>/like/', LikePostAPIView.as_view(), name='like-books'),

    path('comments/<int:comment_id>/like/', LikeCommentAPIView.as_view(), name='like-comment'),
]


