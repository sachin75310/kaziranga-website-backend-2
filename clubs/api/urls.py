from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [
    path("", views.list_communities, name="list_communities"),
    path("<int:community_id>/", views.retrieve_community, name="retrieve_community"),
    path("create/", views.create_community, name="create_community"),
    path("<int:community_id>/update/", views.update_community, name="update_community"),
    path("<int:community_id>/delete/", views.delete_community, name="delete_community"),
]
