from django.urls import path
from . import views

app_name="hall_of_fame"
urlpatterns = [
    path('get-achievements/', views.get_achievements, name='get_achievements'),
    path('get-detailed-achievement/<int:achievement_id>/', views.get_detailed_achievement, name="get_detailed_achievement"),
    path('submit-my-achievement/', views.submit_my_achievements, name='submit_my_achievements')
]
