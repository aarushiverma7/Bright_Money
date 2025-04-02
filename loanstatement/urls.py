from django.urls import path
from .views import GetLoanStatementAPIView

urlpatterns = [
    path('get-statement/', GetLoanStatementAPIView.as_view()),
]
