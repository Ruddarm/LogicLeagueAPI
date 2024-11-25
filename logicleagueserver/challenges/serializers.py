from rest_framework import serializers
from .models import Challenges

class CreateChalllengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenges
        fields = "__all__"
        extra_kwargs = {
            "createdBy": {"read_only": True},  # Make `createdBy` read-only
        }

        
    def create(self,validChallenge,user):
        print(validChallenge)
        return Challenges.objects.create(createdBy=user,**validChallenge)
        