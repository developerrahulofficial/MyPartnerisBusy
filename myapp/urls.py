from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('make_call/', views.make_call, name='make_call'),
    path('twilio_webhook/', views.twilio_webhook, name='twilio_webhook'),
    path('check_call_status/', views.check_call_status, name='check_call_status'),
    ]