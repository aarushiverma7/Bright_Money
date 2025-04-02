from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('loanapp.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('loanstatement.urls')),

]
