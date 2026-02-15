from django.db import models
from student_profile.models import Student

class Achievement(models.Model):

    ACHIEVEMENT_TAG = [
        ("Study", "Study"),
        ("DSA", "DSA"),
        ("Development", "Development"),
        ("Hackathon", "Hackathon"),
        ("Research", "Research"),
        ("Internship", "Internship"),
        ("Job", "Job"),
        ("Contest Win", "Contest Win"),
        ("Misc", "Misc")
    ]
    
    achiever = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="achievements")
    cover_img = models.URLField()
    headline = models.CharField(max_length=150)
    article = models.TextField()
    achievement = models.CharField(max_length=50)
    achievement_tag = models.CharField(max_length=20, choices=ACHIEVEMENT_TAG)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.achiever} | {self.achievement}"
