from django.db import models

class Community(models.Model):
    """
    Model to represent an internal community (club) in Kaziranga.
    Includes details like name, head, member count, description, and status.
    """
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
    ]
    
    THEME_CHOICES = [
        ('CHESS', 'Chess'),
        ('PROGRAMMING', 'Programming'),
        ('SPIRITUALITY', 'Spirituality'),
        ('POETRY', 'Poetry'),
        ('MUSIC', 'Music'),
        ('SPORTS', 'Sports'),
        ('ARTS', 'Arts'),
        ('DEBATE', 'Debate'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    head = models.CharField(max_length=100)
    member_count = models.IntegerField(default=0)
    description = models.TextField(help_text="Rich text description (supports HTML/Markdown)")
    join_form_link = models.URLField(max_length=500)
    logo = models.URLField(max_length=500)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='OTHER')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Communities"
        ordering = ['-created_on']
    
    def __str__(self):
        return f"{self.id}: {self.name} ({self.status})"
