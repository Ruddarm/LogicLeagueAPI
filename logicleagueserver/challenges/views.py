from django.shortcuts import render
import tarfile
import io
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import LogicLeagueUser
from .models import Challenges;
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CreateChalllengeSerializer
import docker
from .Containerpool import  container_pool
import os

# client = docker.from_env()
def create_tarball(code, file_name):
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        file_info = tarfile.TarInfo(file_name)
        file_info.size = len(code)
        tar.addfile(file_info, io.BytesIO(code.encode('utf-8')))
    
    tar_stream.seek(0)
    return tar_stream

class ChallengeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
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
        
        
class testCaseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        user = request.user;
        ChallengeId = request.data["challengeID"]
        challenge = get_object_or_404(Challenges,id=ChallengeId)
        print(challenge)
    
class SolutionHandle(APIView):
    permission_classes = [IsAuthenticated]

    
    def post(self, request, *args, **kwargs):
        output = ""
        error=""
        try:
       # Create a Docker client
            client = docker.from_env()
            code = request.data['code']
            container = container_pool.get_container()
            file_path = "script.py"
            container.put_archive("/sandbox", create_tarball(code=code, file_name=  "Solution.py"))
            container.put_archive("/sandbox",create_tarball(code="21\n18\n",file_name="input.txt"))
            exec_result = container.exec_run("/bin/sh -c 'python3 /sandbox/Solution.py < /sandbox/input.txt 2> /sandbox/error.log'") 
            # exec_result = container.exec_run("/bin/sh -c 'javac Solution.java && java Solution < /sandbox/input.txt'") 
            # java": "javac Solution.java && java Solution"           
            output = exec_result.output.decode("utf-8")
            if exec_result.exit_code!=0:
                error = container.exec_run("cat /sandbox/error.log").output.decode('utf-8');
            container_pool.return_container(container=container)
            # output = exec_result.output.decode("utf-8")  # Standard output from the command
        except Exception as e:
            print("got error")
            print(e)
            error = f"Error: {str(e)}"
            return Response({"error":error},status=status.HTTP_400_BAD_REQUEST);

        return Response({"output": output,"error":error}, status=200)