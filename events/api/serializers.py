from events.models import Event
from student_profile.models import Student
from rest_framework import serializers
from student_profile.api.serializers import StudentSerializer, StudentMiniSerializer

class EventSerializer(serializers.ModelSerializer):
    organizers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all(), write_only=True
    )
    organizers_info = StudentMiniSerializer(source="organizers", many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ["name", "description", "rules", "cover_img", "start_date", "end_date", "prizes", "organizers", "organizers_info", "event_status", "event_tags", "open_to_choices", "event_location", "created_on"]
    
    def create(self, validated_data):
        request = self.context.get("request")
        if request:
            validated_data["created_by"] = request.user
        
        return super().create(validated_data)
