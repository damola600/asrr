# user_events/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path(
        "google/connect/",
        views.google_connect,
        name="google_connect"
    ),

    path(
        "google/callback/",
        views.google_callback,
        name="google_callback"
    ),
    
    path(
        "google/status/",
        views.google_calendar_status,
        name="google_calendar_status"
    ),
]