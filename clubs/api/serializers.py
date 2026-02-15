from rest_framework import serializers
from clubs.models import Community
from events.models import Event


class CommunityEventSerializer(serializers.ModelSerializer):
    """Lightweight event serializer for community details"""
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'start_date', 'end_date', 'event_status', 'event_location']


class CommunityListSerializer(serializers.ModelSerializer):
    """Serializer for listing communities - returns name, logo, member_count, and theme"""
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'logo', 'member_count', 'theme', 'status']


class CommunityDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single community with all fields including events"""
    events = CommunityEventSerializer(many=True, read_only=True)
    
    class Meta:
        model = Community
        fields = [
            'id', 
            'name', 
            'head', 
            'member_count', 
            'description', 
            'join_form_link', 
            'logo', 
            'status', 
            'theme',
            'events',
            'created_on',
            'updated_on'
        ]
