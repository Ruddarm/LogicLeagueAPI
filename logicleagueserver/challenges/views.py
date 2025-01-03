from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import LogicLeagueUser
from .models import Challenges,TestCase
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CreateChalllengeSerializer,TestCaseSerializer
from .Containerpool import  container_pool
from  .CodeExecution import run_code


# Admin views
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
        # try :
        #     challenge_model_data = Challenges.objects.values("challengeID","challengeName",'challengeLevel');
        #     challenge_data = [{"challengeID":str(c['challengeID']),"challengeName":c['challengeName'],"challengeLevel":c['challengeLevel']} for c in challenge_model_data]
        # except Exception as ex :
        #     return Response ({"error":str(ex)} , status=status.HTTP_400_BAD_REQUEST)
        # return Response({"challenges":challenge_data},status=status.HTTP_200_OK)
    
# non admin views
class Challenge(APIView):
    permission_classes =[AllowAny]
    def post():
        pass
    def get(self,request,challengeID=None,*args,**kwargs):
        # a6401008-75a9-4beb-a3c6-d98b290f088d
        if challengeID:
            challenge = get_object_or_404(Challenges,challengeID=challengeID)
            return Response({"challenge":{"challengeName":challenge.challengeName,
                                      "challengeDesc":challenge.challengeDesc,
                                      "challengeLevel":challenge.challengeLevel,
                                      "problemStatement":challenge.problemStatement,
                                      "inputFormat":challenge.inputFormat,
                                      "outputFormat":challenge.outputFormat,
                                      "constraints":challenge.constraints,
                                      }},status=status.HTTP_200_OK)    
        else:
            try :
                challenge_model_data = Challenges.objects.values("challengeID","challengeName",'challengeLevel');
                challenge_data = [{"challengeID":str(c['challengeID']),"challengeName":c['challengeName'],"challengeLevel":c['challengeLevel']} for c in challenge_model_data]
            except Exception as ex :
                return Response ({"error":str(ex)} , status=status.HTTP_400_BAD_REQUEST)
            return Response({"challenges":challenge_data},status=status.HTTP_200_OK)
            
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

# admin views
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
    # Get test cases for challenge  to edit /view
    def get(self,request,challengeID,edit=0,testCaseID=None,*args,**kwargs):
        if challengeID:
            if  edit:
                test_case = get_object_or_404(TestCase,testCaseID=testCaseID)
                data = {"testCaseID": test_case.testCaseID, "input": test_case.input, "output": test_case.output,"marks":test_case.marks,"isSample":test_case.isSample,"explaination":test_case.explaination} 
                return Response (
                {"testCase":data}
                , status=status.HTTP_200_OK
                )
            test_case_data = TestCase.objects.filter(challengeID__challengeID=challengeID)
            test_case = [{"testCaseId":tc.testCaseID,"marks":tc.marks,"isSample":tc.isSample} for tc in test_case_data]
            return Response({"testCases":test_case},
                            status=status.HTTP_200_OK)
        return Response({"msg":"Invalid Challenge ID"} ,status=status.HTTP_400_BAD_REQUEST)
    # To update test case 
    def put(self,request,challengeID,testCaseID):
        if testCaseID:
            test_case_instance = get_object_or_404(TestCase,testCaseID=testCaseID)        
            if test_case_instance:
                test_case_serialized = TestCaseSerializer(test_case_instance ,data=request.data["testCase"])
                if(test_case_serialized.is_valid()):
                    test_case_serialized.save()
                    return Response({"msg":"Updated Sucessfully"},status=status.HTTP_200_OK )
                else:
                    return Response({"error":test_case_serialized.error_messages},status=status.HTTP_400_BAD_REQUEST)
                            
    # to delte testcase 
    def delete(self,request,challengeID,testCaseID=None):
        if testCaseID:
            try:
                test_case = TestCase.objects.get(challengeID__challengeID=challengeID, testCaseID=testCaseID)
                test_case.delete();
                return Response({"msg":"Deleted Sucessfully"}, status=status.HTTP_200_OK)
            except Exception as ex :
                return Response({"error":f'{str(ex)}'}, status= status.HTTP_400_BAD_REQUEST)
        return Response({"msg":f'tescase is required{testCaseID}'},status=status.HTTP_400_BAD_REQUEST)
                
            
                
#To fetch test cases for play ground 
@api_view(['GET'])
def get_test_case_view(request, challengeID):
    
    if challengeID:
        # Fetch test cases for the given challenge ID
        test_cases = TestCase.objects.filter(challengeID__challengeID=challengeID)

        if not test_cases.exists():
            return Response(
                {"msg": "No test cases found for the given Challenge ID."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Prepare the data
        data = [
            {
                "testCaseID": str(tc.testCaseID),
                "input": tc.input,
                "output": tc.output,
            }
            for tc in test_cases
        ]
        return Response({"testCases": data}, status=status.HTTP_200_OK)
    # Invalid challengeID
    return Response({"msg": "Invalid Challenge ID"}, status=status.HTTP_400_BAD_REQUEST)
    
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
        
        