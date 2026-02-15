from django.urls import path
from . import views

app_name = "student_profile"
urlpatterns = [
    path("get-profile/<int:profile_id>/", views.get_profile, name="get_profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile")
]
