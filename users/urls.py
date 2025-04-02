from django.urls import path
from .views import RegisterUserAPIView

urlpatterns = [
    path('register-user/', RegisterUserAPIView.as_view()),
]
