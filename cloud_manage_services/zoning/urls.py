"""
    File Name       : urls.py
    Description     ：
    Author          : mxm
    Created on      : 2020/11/20
"""

from django.urls import path
from zoning import views

urlpatterns = [
    path('create/', views.ZoningCreate.as_view()),
    path('update/', views.ZoningUpdate.as_view()),
    path('delete/', views.ZoningDelete.as_view()),
    path('detail/', views.ZoningDetail.as_view()),
    path('list/', views.ZoningList.as_view()),
]