from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import AnnouncementSerializer
from .permissions import IsAdminOrStaff
from announcements.models import Announcement
from .pagination import AnnouncementPaginator
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied

@api_view(["GET"])
def list_announcements(request):
    try:
        announcements = Announcement.objects.all()
        
        paginator = AnnouncementPaginator()
        paginated_announcements = paginator.paginate_queryset(announcements, request)
        serializer = AnnouncementSerializer(paginated_announcements, many=True)

        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({"error": "Some error occured, Announcements could not be found"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def retrieve_announcement(request, announcement_id):
    try:
        announcement = Announcement.objects.get(id=announcement_id)

        serializer = AnnouncementSerializer(announcement)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Announcement.DoesNotExist:
        return Response({"error": "Announcement Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occured, Announcement could not be found"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminOrStaff])
def create_announcement(request):
    try:
        
        required_fields = ["title"]

        if request.data["help_format"] == 1:
            required_fields += ["intro", "category", "target_audience", "use_case", "summary"]
            missing_fields = [field for field in required_fields if field not in request.data]
            if missing_fields:
                return Response({"message": f"Missing fields: {missing_fields}"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data["help_format"] == 0:
            if "message" not in request.data:
                return Response({"message": f"Missing fields: [message]"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AnnouncementSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Announcement created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except PermissionDenied:
        return Response({"error": "You don't have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({"error": "An error occured, Announcement could not be found"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
