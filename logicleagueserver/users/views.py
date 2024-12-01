from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import LogicLeagueUser
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.authentication import JWTAuthentication

from google.oauth2 import id_token
import requests



class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        # print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            LogicLeagueUser = serializer.save()
            print(LogicLeagueUser)
            return Response({"message":"done dona done "},status=status.HTTP_201_CREATED)
        else:
            print("not valid")
        return Response({"msg":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        print(request.data);
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.get_token(user)
            response = Response({
                "messagse":"Login Success full",
                "user":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,   
                }},
                                status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=str(tokens["access"]),
                httponly=True,
                secure=False ,
                samesite="Lax",
                max_age=7*24*60*60*1000
            )
            response.set_cookie(
                key="refresh_token",
                value=str(tokens["refresh"]),
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite="Lax",
                max_age=7*24*60*60*1000
            )
            return response;
                
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
class getName(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print(request.COOKIES)
        return Response({"msg":"Welcome to home page"},status=status.HTTP_200_OK)
    

class GoogleLogin(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        access_token = request.data.get("token")
        if not access_token:
            return Response({"Error":"Token not provided"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user_info_response = requests.get( "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"})
            if user_info_response.status_code != 200:
                return Response({"Error": "Failed to fetch user info from Google"}, status=status.HTTP_400_BAD_REQUEST)
            user_info = user_info_response.json()
            email = user_info["email"]
            name = user_info["name"]
            if not email:
                return Response({"Error":"Invalid Email"},status=status.HTTP_400_BAD_REQUEST)
            user,created = LogicLeagueUser.objects.get_or_create(email=email)
            if created:
                user.username = name
                user.set_unusable_password()  # No password since this is a social login
                user.save()
            refresh = RefreshToken.for_user(user)
            tokens = {
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
            }
            response = Response({
                "messagse":"Login Success full",
                "user":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,   
                }},
                                status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=str(tokens["access"]),
                httponly=True,
                secure=False ,
                samesite="Lax",
                max_age=7*24*60*60*1000
            )
            response.set_cookie(
                key="refresh_token",
                value=str(tokens["refresh"]),
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite="Lax",
                max_age=7*24*60*60*1000
            )
            return response;
        except ValueError:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        response = Response({"message": "Logged out successfully!"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
