from django.db import models
from student_profile.models import Student
from clubs.models import Community

class Event(models.Model):

    EVENT_STATUS_CHOICES = [
        ("LIVE", "Live"),
        ("UPCOMING", "Upcoming"),
        ("ENDED", "Ended")
    ]
    EVENT_TAGS = [
        ("HACKATHON", "Hackathon"),
        ("DSA", "DSA"),
        ("UI/UX", "UI/UX"),
        ("IDEATION", "Ideation")
    ]
    OPEN_TO_CHOICES = [
        ("OPEN", "Open to Everyone"),
        ("KAZIRANGA", "Kaziranga Only"),
        ("BS", "BS Degree Students"),
        ("ALL", "All")
    ]
    EVENT_LOCATION = [
        ("ONLINE", "Online"),
        ("OFFLINE", "Offline"),
        ("HYBRID", "Hybrid")
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    rules = models.JSONField(default=list, blank=True)
    cover_img = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    prizes = models.JSONField(default=list, blank=True)
    organizers = models.ManyToManyField(Student, related_name="organized_events")
    event_status = models.CharField(max_length=15, choices=EVENT_STATUS_CHOICES, default="")
    event_tags = models.CharField(max_length=15, choices=EVENT_TAGS, default="")
    open_to_choices = models.CharField(max_length=20, choices=OPEN_TO_CHOICES, default="")
    event_location = models.CharField(max_length=20, choices=EVENT_LOCATION, default="")
    created_by = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="created_events")
    created_on = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")

    def __str__(self):
        return f"{self.id}: {self.name}"
