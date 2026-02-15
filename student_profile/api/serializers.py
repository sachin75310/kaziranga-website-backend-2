from rest_framework import serializers
from student_profile.models import Student

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        exclude = ["password", "last_login", "is_superuser", "is_staff", "is_active", "groups", "user_permissions"]

class StudentMiniSerializer(serializers.ModelSerializer):

    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "username", "profile_pic", "profile_url"]
    
    def get_profile_url(self, obj):
        return f"https://kaziranga-house/student-profile/{obj.username}"
