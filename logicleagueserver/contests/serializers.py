from rest_framework import serializers
from .models import Contest , ContestChallenge


class ContestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['name']
        
class ContestEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['name', 'description', 'start_time', 'end_time', 'prizes']
        extra_kwargs = {'name': {'required': False}}  
        
class ContestChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestChallenge
        fields = ['challenge', 'marks']