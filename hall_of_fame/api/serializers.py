from rest_framework import serializers
from hall_of_fame.models import Achievement
from student_profile.api.serializers import StudentMiniSerializer

class AchievementCoverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        exclude = ["achiever", "article", "achievement"]

class AchievementSerializer(serializers.ModelSerializer):
    achiever = StudentMiniSerializer(read_only=True)

    class Meta:
        model = Achievement
        fields = "__all__"
    
    def validate_achievement_tag(self, value):
        valid_tags = [tag[0] for tag in Achievement.ACHIEVEMENT_TAG]
        if value not in valid_tags:
            raise serializers.ValidationError("Invalid achievement tag.")
        return value
    
    def create(self, validated_data):
        request = self.context.get("request")

        if request:
            validated_data["achiever"] = request.user.id
        return super().create(validated_data)
