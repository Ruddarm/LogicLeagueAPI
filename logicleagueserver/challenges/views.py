from django.shortcuts import render
from rest_framework.response import Response
from .models import Challenges;
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CreateChalllengeSerializer

class ChallengeCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = CreateChalllengeSerializer(data=request.data)
        if serializer.validate(serializer):
            print(serializer)
            return Response({"Msg":"working"},status=status.HTTP_200_OK)
        else:
            return Response({"Msg":"Nhai hua "}, status=status.HTTP_400_BAD_REQUEST)