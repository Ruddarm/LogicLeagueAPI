from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import LogicLeagueUser
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        # print(request.data)
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            LogicLeagueUser = serializer.save()
            print(LogicLeagueUser)
            return Response({"message":"done dona done "},status=status.HTTP_201_CREATED)
        else:
            print("not valid")
        return Response({"msg":str(serializer.errors)},status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.get_token(user)
            return Response({
                "messagse":"Login Sucess full",
                "tokens":tokens,
                "user":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                },
                
            },
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class getName(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        return Response({"msg":"haa bhia sab mastt"},status=status.HTTP_200_OK)