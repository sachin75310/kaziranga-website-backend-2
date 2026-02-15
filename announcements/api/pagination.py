from rest_framework.pagination import PageNumberPagination

class AnnouncementPaginator(PageNumberPagination):
    page_size = 10
