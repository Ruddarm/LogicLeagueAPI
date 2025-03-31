from rest_framework import serializers
from .models import Contest , ContestChallenge


class ContestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['name']
        
class ContestEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['name', 'description', 'start_time', 'end_time', 'prizes' , "scoring","rules"]
        extra_kwargs = {'name': {'required': False}}  
        
class ContestChallengeSerializer(serializers.ModelSerializer):
    challenge_name = serializers.SerializerMethodField()  
    class Meta:
        model = ContestChallenge
        fields = ['challenge', 'marks','challenge_name']
    def get_challenge_name(self, obj):
        return obj.challenge.challengeName if obj.challenge else None
class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ["id", "name", "start_time"]