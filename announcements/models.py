from django.db import models
from student_profile.models import Student

class Announcement(models.Model):
    """
    Model to represent an announcement.
    Includes details like author, title, category, message, and timestamp.
    """
    class Category(models.TextChoices):
        EDUCATIONAL = 'E', 'Educational'
        MEETUP = 'M', 'Meetup'
        CLUB = 'C', 'Club'
        MISC = 'MI', 'Miscellaneous'
        EVENT = 'Ev', 'Event'
    
    class StudyLevel(models.TextChoices):
        FOUNDATION = 'FL', 'Foundation'
        DIPLOMA_P = 'DP', 'Diploma(Programming)'
        DIPLOMA_S = 'DS', 'Diploma(Data Science)'
        BSC = 'BSC', 'BSc'
        BS = 'BS', 'BS'
        ALL = 'All', 'All Levels'
    
    class HelpFormat(models.IntegerChoices):
        ON = 1, 'On'
        OFF = 0, 'Off'

    author = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, unique=True)
    help_format = models.BooleanField(choices=HelpFormat.choices, default=HelpFormat.ON)
    intro = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=2,choices=Category.choices, default=Category.MISC, blank=True)
    target_audience = models.CharField(max_length=21, choices=StudyLevel.choices, default=StudyLevel.ALL, blank=True)
    use_case = models.CharField(max_length=200, blank=True)
    summary = models.CharField(max_length=150, blank=True)
    message = models.TextField(max_length=500, blank=True)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Id #{self.id} by {self.author}"