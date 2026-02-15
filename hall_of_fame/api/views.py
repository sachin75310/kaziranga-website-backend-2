from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .pagination import AchievementPaginator
from hall_of_fame.models import Achievement
from .serializers import AchievementSerializer, AchievementCoverSerializer

@api_view(["GET"])
def get_achievements(request):
    try:
        achievements = Achievement.objects.all()

        paginator = AchievementPaginator()
        paginated_achievements = paginator.paginate_queryset(achievements, request)
        serializer = AchievementCoverSerializer(paginated_achievements, many=True)

        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({"error": "An error occured, couldn't get achievement list"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def get_detailed_achievement(request, achievement_id):
    try:
        achievement = Achievement.objects.get(id=achievement_id)

        serializer = AchievementSerializer(achievement)

        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

    except Achievement.DoesNotExist:
        return Response({"message": "Achievement Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occured, couldn't get achievement article"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_my_achievements(request):
    try:
        student = request.user

        if not student:
            return Response(
                {"error": "Student profile not found for this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AchievementSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            Achievement.objects.create(
                achiever=student,
                **serializer.validated_data
            )
            return Response({"message": "Achievement submitted successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An error occured, couldn't submit achievement"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
