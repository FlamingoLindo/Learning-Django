from django.urls import path
from .views import (MyTokenObtainPairView, get_users, create_user, user_detail, login, 
                    create_point, get_points, point_detail, review_point, review_detail, get_all_reviews,
                    point_reviews)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', get_users, name='get_users'),
    path('users/create/', create_user, name='create_user'),
    path('user/<int:pk>/', user_detail, name='user_detail'),
    path('login/', login, name='login'),

    path('points/', get_points, name='get_points'),
    path('points/create/', create_point, name='create_point'),
    path('point/<int:pk>/', point_detail, name='point_detail'),
    path('point/<int:pk>/reviews/', point_reviews, name='point_reviews'),

    path('review/create/', review_point, name='review_point'),
    path('reviews/', get_all_reviews, name='get_reviews'),
    path('review/<int:pk>/', review_detail, name='review_detail'),
]