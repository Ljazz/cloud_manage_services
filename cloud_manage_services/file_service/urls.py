"""
    File Name       : urls.py
    Description     ：
    Author          : mxm
    Created on      : 2020/7/13
"""

from django.urls import path
from file_service import views

urlpatterns = [
    path('upload/', views.FileUpload.as_view()),
    path('downLoad/', views.FileDownLoad.as_view()),
    path('delete/', views.FileDelete.as_view()),
]
