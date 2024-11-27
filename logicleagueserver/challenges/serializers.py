from rest_framework import serializers
from .models import Challenges,Solution,TestCase

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
    
class CreateTestCase(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields= "__all__"
        read_only_fields= ["testCaseID"]
    def validate(self, attrs):
        if  not attrs :
            raise serializers.ValidationError("Test Case required")
        if not attrs.input:
            raise serializers.ValidationError("Input is required")
        if not attrs.output:
            raise serializers.ValidationError("Outpur is required")
        return  attrs

    