from django.urls import path
from .views import CustomLoginView, UserRegistrationView, LogoutView

urlpatterns = [
    path('login/', CustomLoginView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
