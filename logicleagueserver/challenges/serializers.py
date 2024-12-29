from rest_framework import serializers
from .models import Challenges,Solution,TestCase

import ast  
class CreateChalllengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenges
        fields = ["challengeName", "challengeLevel","problemStatement","inputFormat","outputFormat","constraints"]
        extra_kwargs = {
            "ChallengeId":{"read_only":True},
            "createdBy": {"read_only": True},
            "challengeDesc":{"required",False}
            
        }
    def create(self,validChallenge,user):
        print("valid challenge",validChallenge)
        return Challenges.objects.create(createdBy=user,**validChallenge)
    
class TestCaseSerializer(serializers.ModelSerializer):
    input = serializers.JSONField(write_only=True)  # Input will be provided as JSON
    output = serializers.CharField()
    explaination = serializers.CharField(allow_blank=True, required=False)
    isSample = serializers.BooleanField(default=False)
    marks = serializers.IntegerField(default=0)

    class Meta:
        model = TestCase
        fields = ['testCaseID', 'input', 'output', 'explaination', 'isSample', 'marks', 'challengeID']
        
    def validate(self, attrs):
        if  not attrs :
            raise serializers.ValidationError("Test Case required")
        if not attrs['input']:
            raise serializers.ValidationError("Input is required")
        if not attrs['output']:
            raise serializers.ValidationError("Outpur is required")
        return  attrs
    def create(self, validated_data):
        # Generate `input_txt` from variables and values
        input_values = []
        for item in validated_data["input"]:
            value = item["value"]
            if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                try:
            # Safely parse the string to a Python list
                    parsed_value = ast.literal_eval(value)
                    if isinstance(parsed_value, list):
                        input_values.extend(map(str, parsed_value))
                    else:
                        input_values.append(value)  # If parsing fails, treat as string
                except (ValueError, SyntaxError):
                    input_values.append(value)  
            else:
                input_values.append(str(value))
        text_content = "\n".join(input_values)
        validated_data['input_txt'] = text_content;
        validated_data['output_txt'] = validated_data['output']+"\n"
        return TestCase.objects.create(**validated_data)
         