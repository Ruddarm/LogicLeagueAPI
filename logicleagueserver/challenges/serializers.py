from rest_framework import serializers
from .models import Challenges

class CreateChalllengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenges
        fields = "__all__"
        read_only_fields=[]
        
    def create(self,validChallenge):
        print(validChallenge)
        return Challenges.objects.create(**validChallenge)
        