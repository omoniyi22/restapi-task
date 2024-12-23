# project_name/urls.py (usually the folder containing settings.py)
from django.contrib import admin
from django.urls import path, include  # include is required to add app URLs


urlpatterns = [
    path("admin/", admin.site.urls),  # Django Admin URL
    path(r'api/', include("news.urls")),  # Include the news app URLs
]
