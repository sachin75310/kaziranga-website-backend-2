from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from student_profile.models import Student
from student_profile.api.serializers import StudentSerializer
from .serializers import EventSerializer
from events.models import Event
from .pagination import EventPaginator
from .permissions import IsAdminOrStaff

# Make sure this works
@api_view(["POST"])
@permission_classes([IsAuthenticated & IsAdminOrStaff])
def create_event(request):
    try:
        required_fields = ["name", "description", "rules", "cover_img", "start_date", "end_date", "prizes", "organizers", "event_status", "event_tags", "open_to_choices", "event_location"]

        missing_fields = [field for field in required_fields if field not in request.data]

        if missing_fields:
            return Response({"message": f"Missing fields: {missing_fields}"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(request.data["prizes"], list):
            return Response({"message": "Prizes must be a list"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(request.data["rules"], list):
            return Response({"message": "Rules must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Student.DoesNotExist:
        return Response({"error": "Student Not Found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An error occured, couldn't create event"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def get_events(request):
    try:
        event_status = request.query_params.get("event-status")
        event_tag = request.query_params.get("event-tag")
        open_to_choice = request.query_params.get("open-to-choice")
        event_location = request.query_params.get("event-location")

        events = Event.objects.all()

        if event_status:
            if event_status.upper() in [event_model_status[0] for event_model_status in Event.EVENT_STATUS_CHOICES]:
                events = events.filter(event_status=event_status.upper())
            else:
                return Response({"message": "Incorrect event status"}, status=status.HTTP_400_BAD_REQUEST)
        if event_tag:
            if event_tag.upper() in [event_model_tag[0] for event_model_tag in Event.EVENT_TAGS]:
                events = events.filter(event_tags=event_tag.upper())
            else:
                return Response({"message": "Incorrect event tag"}, status=status.HTTP_400_BAD_REQUEST)
        if open_to_choice:
            if open_to_choice.upper() in [event_model_open_to_choice[0] for event_model_open_to_choice in Event.OPEN_TO_CHOICES]:
                events = events.filter(open_to_choices=open_to_choice.upper())
            else:
                return Response({"message": "Incorrect event eligibility"}, status=status.HTTP_400_BAD_REQUEST)
        if event_location:
            if event_location.upper() in [event_model_location[0] for event_model_location in Event.EVENT_LOCATION]:
                events = events.filter(event_location=event_location.upper())
            else:
                return Response({"message": "Incorrect event location"}, status=status.HTTP_400_BAD_REQUEST)

        paginator = EventPaginator()
        paginated_events = paginator.paginate_queryset(events, request)

        serializer = EventSerializer(paginated_events, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({"error": "An error occured, couldn't get event details"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(["GET"])
def view_event(request, event_id):

    try:
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response({"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occured, couldn't get event details"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
