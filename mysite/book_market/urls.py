from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'favorite', FavoriteAPIView, basename='favorite')
router.register(r'favorite_item', FavoriteItemAPIView, basename='favorite_item')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileEditAPIView.as_view(), name='user_edit'),
    path('user/following/', SubscriptionUserListAPIView.as_view(), name='user_following'),
    path('user/following/<int:pk>/', SubscriptionUserDetailAPIView.as_view(), name='user_following_detail'),

    path('market/', MarketListAPIView.as_view(), name='market_list'),
    path('market/<int:pk>/', MarketDetailAPIView.as_view(), name='market_detail'),
    path('market/create/', MarketCreateAPIView.as_view(), name='market_create'),
    path('market_list/', MarketOwnAPIView.as_view(), name='market_own_list'),
    path('market_list/<int:pk>/', MarketEditAPIView.as_view(), name='market_own_edit'),
    path('market_list/<int:market_id>/follower/', SubscriptionMarketAPIView.as_view(), name='market_follower'),
    # path('market_list/<int:market_id>/follower/', SubscriptionMarketDetailAPIView.as_view(), name='market_follower_detail'),

    path('book/', BookListAPIView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailAPIView.as_view(), name='book_detail'),
    path('book/create/', BookCreateAPIView.as_view(), name='book_create'),
    path('book_list/<int:pk>/', BookOwnEditAPIView.as_view(), name='book_own_edit'),

    path('market/follow/<int:market_id>/', toggle_follow, name='toggle_subscription'),
    path('book/like/<int:book_id>/', toggle_book_like, name='toggle_subscription'),
    path('comment/like/<int:comment_id>/', toggle_comment_like, name='toggle_comment_like'),

    path('branch/create/', BranchCreateAPIView.as_view(), name='branch_create'),
    path('branch/<int:pk>/', BranchEditAPIView.as_view(), name='branch_edit'),

    path('contact/create/', ContactCreateAPIView.as_view(), name='contact_create'),
    path('contact/<int:pk>/', ContactEditAPIView.as_view(), name='contact_edit'),

    path('comment/create/', CommentCreateAPIView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', CommentDeleteAPIView.as_view(), name='comment_delete'),

    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
