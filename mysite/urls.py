from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("complaints_management_system.urls")),
]


# handler404 = 'complaints_management_system.views.error_404_view'
