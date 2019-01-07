from django.urls import path, re_path
from . import views
from django.shortcuts import redirect
from .models import Event

app_name = 'event'

urlpatterns = [
    path('', views.event_list, name='events'),
    path('<int:id>/', views.event_detail, name='event_detail'),
    path('contact/', views.contact, name='contact'),
    path('send_email/', views.send_email, name='send_email'),
]
