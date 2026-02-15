from announcements.models import Announcement
from student_profile.api.serializers import StudentMiniSerializer
from rest_framework import serializers

class AnnouncementSerializer(serializers.ModelSerializer):
    author = StudentMiniSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"
    
    def create(self, validated_data):
        request = self.context.get("request")
        if request:
            validated_data["author"] = request.user
        
        return super().create(validated_data)

