from django.urls import path, include
from . import views

urlpatterns = [
    path('download-files/', views.download_files, name='download_files'),
]