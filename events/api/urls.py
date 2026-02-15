from django.urls import path
from . import views

app_name = "events"
urlpatterns = [
    path("create/", views.create_event, name="create_event"),
    path("get-events/", views.get_events, name="get_events"),
    path("get-event/<int:event_id>/", views.view_event, name="view_event")
]
