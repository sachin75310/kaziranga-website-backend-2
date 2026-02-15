from rest_framework.pagination import PageNumberPagination

class AchievementPaginator(PageNumberPagination):
    page_size = 1
