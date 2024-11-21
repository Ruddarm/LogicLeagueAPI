from rest_framework import serializers
from .models import LogicLeagueUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicLeagueUser
        fields= ['id','username','email']
        read_only_fields=['id']
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicLeagueUser
        fields = ['username','email','password']
        extra_kwargs = {'password':{"write_only":True}}
    def create(self, validated_data):
        print(validated_data)
        return LogicLeagueUser.objects.create_user(validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=LogicLeagueUser
        fields=['email','password']
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)
    def validate(self, attrs):
        email = attrs['email']
        password = attrs.get('password')
        
        user = authenticate(email=email,password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        attrs['user']=user
        return attrs
    def get_token(self,user):
        refresh = RefreshToken.for_user(user=user)
        return{
            "refresh":str(refresh),
            "access":str(refresh.access_token),
        }