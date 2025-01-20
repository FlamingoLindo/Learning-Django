from django.urls import path
from .views import (MyTokenObtainPairView, get_users, create_user, user_detail, login, 
                    create_point, get_points)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', get_users, name='get_users'),
    path('users/create/', create_user, name='create_user'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('login/', login, name='login'),

    path('points/', get_points, name='get_points'),
    path('points/create/', create_point, name='create_point'),
]


# JWT IN USER CREATION
# SEE WHY POINTS ARE NOT SHOWING UP ON USER
# ADD AUTHENTICATION TO CALLS