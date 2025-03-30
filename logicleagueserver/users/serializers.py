from rest_framework import serializers
from .models import LogicLeagueUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

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
    def decode_token(self,request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "): 
            raise AuthenticationFailed("Invalid Authenication")
        

class UpdatePassSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your old password is incorrect.")
        return value

    def validate_new_password(self, value):
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']
        user.update_pass(old_password, new_password)

class UpdateUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(write_only=True, max_length=50)
    def validate_new_username(self, value):
        if LogicLeagueUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("The username is already taken.")
        return value
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
    def save(self, **kwargs):
        user = self.context['request'].user
        new_username = self.validated_data['new_username']
        user.update_username(new_username)
        