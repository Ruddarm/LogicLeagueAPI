from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import LogicLeagueUser
from .models import Challenges;
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CreateChalllengeSerializer

class ChallengeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        print(user.id)
        logicLeagueUser = get_object_or_404(LogicLeagueUser, id = user.id)
        print(logicLeagueUser)
        # request.data["createdBy"]=logicLeagueUser.id; 
        serializer = CreateChalllengeSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer)
            serializer.create(serializer.data,logicLeagueUser)
            return Response({"Msg":"working"},status=status.HTTP_200_OK)
        else:
            return Response({ "msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)