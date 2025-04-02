from rest_framework import serializers
from .models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'aadhar_id', 'name', 'email', 'annual_income']
