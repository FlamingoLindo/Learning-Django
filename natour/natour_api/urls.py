from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.auth import MyTokenObtainPairView, create_user, login
from .views.users import get_users, user_detail
from .views.points import create_point, get_points, point_detail
from .views.reviews import review_point, review_detail, get_all_reviews,  point_reviews
from .views.dashboard import user_count
from .views.terms import get_term, add_terms, update_terms

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

    path('dashboard/user_count', user_count, name='user_count'),

    path('terms/get_term', get_term, name='get_term'),
    path('terms/add_term', add_terms, name='add_terms'),
    path('terms/update_terms/<int:pk>/', update_terms, name='update_terms')
]

#termos de uso