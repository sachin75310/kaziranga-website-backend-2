from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from student_profile.models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
def get_profile(request, profile_id):
    try:
        student = Student.objects.get(id=profile_id)

        serializer = StudentSerializer(student)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Student.DoesNotExist:
        return Response({"message": "Profile Not Found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"error": "An error occured, couldn't get profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    try:
        student = request.user

        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile Updated"}, status=status.HTTP_200_OK)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        return Response({"error": "An error occured, couldn't edit profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
