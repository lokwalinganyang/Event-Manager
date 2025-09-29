from rest_framework import serializers
from .models import Event, Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'registered_at']

class EventSerializer(serializers.ModelSerializer):
    registered_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 
                 'max_participants', 'registered_count', 'is_full', 
                 'created_at', 'updated_at']

class EventDetailSerializer(EventSerializer):
    registrations = RegistrationSerializer(many=True, read_only=True)
    
    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ['registrations']

class RegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'email', 'phone', 'event']
    
    def validate(self, data):
        event = data['event']
        if event.is_full:
            raise serializers.ValidationError("This event is already full.")
        return data