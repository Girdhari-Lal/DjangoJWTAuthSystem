from django.urls import path
from users.views import UserRegisterView, UserLoginView, UserProfileView
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('user/', UserProfileView.as_view(), name = 'user'),
]
