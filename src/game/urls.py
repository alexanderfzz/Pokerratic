from django.urls import path

from . import views


app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:roomID>/', views.room, name='room'),
]
