from django.urls import path
from . import views

app_name="announcements"
urlpatterns = [
    path("get-announcements/", views.list_announcements, name="announcements"),
    path("announcement/<int:announcement_id>/", views.retrieve_announcement, name="announcement_by_id"),
    path("create/", views.create_announcement, name="create_announcement")
]