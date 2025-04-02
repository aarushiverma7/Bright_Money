from django.urls import path
from .views import ApplyLoanAPIView

urlpatterns = [
    path('apply-loan/', ApplyLoanAPIView.as_view()),
]

