from django.shortcuts import render

import io
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import LogicLeagueUser
from .models import Challenges,TestCase
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CreateChalllengeSerializer,TestCaseSerializer
import docker
from .Containerpool import  container_pool
import os
from  .CodeExecution import run_code

class ChallengeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        user = request.user
        print(user.id)
        print(request.data["ChallengeState"])
        logicLeagueUser = get_object_or_404(LogicLeagueUser, id = user.id)
        # request.data["createdBy"]=logicLeagueUser.id; 
        serializer = CreateChalllengeSerializer(data=request.data["ChallengeState"])
        if serializer.is_valid():
            new_challenge =  serializer.create(serializer.data,logicLeagueUser)
            return Response({"Msg":"Challenge Created Sucessfully","id":new_challenge.challengeID},status=status.HTTP_200_OK)
        else:
            return Response({ "msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,*args,**kwargs):
        pass
    
class Challenge(APIView):
    permission_classes =[AllowAny]
    def post():
        pass
    def get(self,request,challengeID,*args,**kwargs):
        # a6401008-75a9-4beb-a3c6-d98b290f088d
        challenge = get_object_or_404(Challenges,challengeID=challengeID)
        return Response({"challenge":{"challengeName":challenge.challengeName,
                                      "challengeDesc":challenge.challengeDesc,
                                      "challengeLevel":challenge.challengeLevel,
                                      "problemStatement":challenge.problemStatement,
                                      "inputFormat":challenge.inputFormat,
                                      "outputFormat":challenge.outputFormat,
                                      "constraints":challenge.constraints,
                                      }},status=status.HTTP_200_OK)    
    def put(self,request,challengeID,*args,**kwargs):
        data =  request.data["ChallengeState"];
        challenge_instance = get_object_or_404(Challenges,challengeID=challengeID)        
        if challenge_instance:
            print(request.data["ChallengeState"])
            challengeSerializer = CreateChalllengeSerializer(challenge_instance ,data=request.data["ChallengeState"])
            if(challengeSerializer.is_valid()):
                challengeSerializer.save()
                return Response({"msg":"Updated Sucessfully"},status=status.HTTP_200_OK )
        return Response({"msg":"challengeSerializer"},status=status.HTTP_400_BAD_REQUEST)
        
class testCaseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer = TestCaseSerializer(data=request.data.get('testCase', {}))
        if serializer.is_valid():
            test_case = serializer.save()
            return Response({
                "msg": "Test Case Created Successfully",
                "testCaseID": test_case.testCaseID
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,challengeID,*args,**kwargs):
        if challengeID:
            test_cases = TestCase.objects.filter(challengeID__challengeID = challengeID)
            data = [{"testCaseID": str(tc.testCaseID), "input": tc.input, "output": tc.output} for tc in test_cases]
            return Response (
                {"testCases":data}
                , status=status.HTTP_200_OK
            )
        return Response({"msg":"Invalid Challenge ID"} ,status=status.HTTP_400_BAD_REQUEST)
    
class SolutionHandle(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        output = ""
        error=""
        iserror = True
        try:
            code = request.data['code']
            language = request.data['lang']
            result = run_code(code=code,language=language)
            print()
        except Exception as e:
            print("got error")
            print(e)
            error = f"Error: {str(e)}"
            return Response({"error":error},status=status.HTTP_400_BAD_REQUEST);
        
        return Response({"output": result['output'],"error":result['error'] , "isError":result['iserror']}, status=200)
        
        