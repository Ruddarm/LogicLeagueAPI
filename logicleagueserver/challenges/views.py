from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import LogicLeagueUser
from .models import Challenges,TestCase
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CreateChalllengeSerializer,TestCaseSerializer
from .Containerpool import  container_pool
from  .CodeExecution import run_code , submit_code



# Admin views for challenge creation
class challenge_admin_view(APIView):
    permission_classes = [IsAuthenticated]
    # to create challenges
    def post(self,request,*args,**kwargs):
        user = request.user
        logicLeagueUser = get_object_or_404(LogicLeagueUser, id = user.id)
        serializer = CreateChalllengeSerializer(data=request.data["ChallengeState"])
        if serializer.is_valid():
            new_challenge =  serializer.create(serializer.data,logicLeagueUser)
            return Response({"Msg":"Challenge Created Sucessfully","id":new_challenge.challengeID},status=status.HTTP_200_OK)
        else:
            return Response({ "msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    # to get challenge data for admin if required
    def get(self,request,*args,**kwargs):
        pass
    # updata challegne data 
    def put(self,request,challengeID,*args,**kwargs):
        challenge_instance = get_object_or_404(Challenges,challengeID=challengeID)        
        if challenge_instance:
            # print(request.data["ChallengeState"])
            challengeSerializer = CreateChalllengeSerializer(challenge_instance ,data=request.data["ChallengeState"])
            if(challengeSerializer.is_valid()):
                challengeSerializer.save()
                return Response({"msg":"Updated Sucessfully"},status=status.HTTP_200_OK )
        return Response({"msg":"challengeSerializer"},status=status.HTTP_400_BAD_REQUEST)
    # Delete challenge data 
    def delete(self,request,challengeID,*args,**kwargs):
        challenge_instance = get_object_or_404(Challenges,challengeID=challengeID)
        if challenge_instance:
            challenge_instance.delete()
            return Response({"msg":"Deleted Sucessfully"},status=status.HTTP_200_OK)
        return Response({"msg":"Invalid Challenge ID"},status=status.HTTP_400_BAD_REQUEST)
    
# Get Challenge data for users playground dispalay
class challenge_user_view(APIView):
    permission_classes =[AllowAny]
    def get(self,request,challengeID=None,*args,**kwargs):
        # if challenge id return challenge data
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
        # else return all challenges
        else:
            try :
                challenge_model_data = Challenges.objects.values("challengeID","challengeName",'challengeLevel');
                challenge_data = [{"challengeID":str(c['challengeID']),"challengeName":c['challengeName'],"challengeLevel":c['challengeLevel']} for c in challenge_model_data]
            except Exception as ex :
                return Response ({"error":str(ex)} , status=status.HTTP_400_BAD_REQUEST)
            return Response({"challenges":challenge_data},status=status.HTTP_200_OK)
            
# Test case view for admin to create,update,delete test cases
class testcase_admin_view(APIView):
    permission_classes = [IsAuthenticated]
    # Create test case for a challenge
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
            # get test case for a given challenge id and test case id
            if  edit:
                test_case = get_object_or_404(TestCase,testCaseID=testCaseID)
                data = {"testCaseID": test_case.testCaseID, "input": test_case.input, "output": test_case.output,"marks":test_case.marks,"isSample":test_case.isSample,"explaination":test_case.explaination} 
                return Response (
                {"testCase":data}
                , status=status.HTTP_200_OK
                )
            # get all test cases for a given challenge id
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
    # To delete test case
    def delete(self,request,challengeID,testCaseID=None):
        if testCaseID:
            try:
                test_case = TestCase.objects.get(challengeID__challengeID=challengeID, testCaseID=testCaseID)
                test_case.delete();
                return Response({"msg":"Deleted Sucessfully"}, status=status.HTTP_200_OK)
            except Exception as ex :
                return Response({"error":f'{str(ex)}'}, status= status.HTTP_400_BAD_REQUEST)
        return Response({"msg":f'tescase is required{testCaseID}'},status=status.HTTP_400_BAD_REQUEST)
                
            
                
#To fetch test cases for terminal withou explaination
@api_view(['GET'])
@permission_classes([AllowAny]) 
def get_test_case_view_terminal(request, challengeID):
    print("here bsdk")
    if challengeID:
        # Fetch test cases for the given challenge ID
        test_cases = TestCase.objects.filter(challengeID__challengeID=challengeID,isSample=True)
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

# To fetch test cases fo user playground with explaination
@api_view(['GET'])
@permission_classes([AllowAny])
def get_test_case_view_desc(request,challengeID):
    if challengeID:
        test_cases = TestCase.objects.filter(challengeID__challengeID=challengeID,isSample=True)
        if not test_cases.exists():
            return Response(
                {"msg": "No test cases found for the given Challenge ID."},
                status=status.HTTP_404_NOT_FOUND,
            )
        data = [
            {
                "testCaseID": str(tc.testCaseID),
                "input": tc.input,
                "output": tc.output,
                "isSampel":tc.isSample,
                "explainaiton":tc.explaination
            }
            for tc in test_cases
        ]
        return Response({"testCases": data}, status=status.HTTP_200_OK)
    return Response({"msg": "Invalid Challenge ID"}, status=status.HTTP_400_BAD_REQUEST)

# To handle code execution
class SolutionHandle(APIView):
    permission_classes = [AllowAny]
    def post(self, request, challengeID, *args, **kwargs):
        output = ""
        error=""
        iserror = True
        try:
            code = request.data['code']
            language = request.data['lang']
            result = run_code(code=code,language=language, challenge_id=challengeID)
        except Exception as e:
            error = f"Error: {str(e)}"
            return Response({"error":error},status=status.HTTP_400_BAD_REQUEST);
        
        return Response({"result":result['result'],"output": result['output'],"error":result['error'] , "isError":result['iserror']}, status=200)
        
        
# Submit submission for a challenge
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_submission(request,challengeID):
    if challengeID:
        user = request.user
        logicLeagueUser = get_object_or_404(LogicLeagueUser, id = user.id)
        challenge_instance = get_object_or_404(Challenges,challengeID=challengeID)
        # if we get chalelnge instance and user instance
        if challenge_instance and logicLeagueUser:
            try:
                code = request.data['code']
                language = request.data['lang']
                result = submit_code(code=code,language=language, challenge_instance=challenge_instance,user_instance=logicLeagueUser)
                # handeling error 
                print(result)
                if not result['iserror']:
                    # if error not occured
                    # if submission is sucessfull
                    return Response({"result":result['result'],"output": result['output'],"error":result['error'] , "isError":result['iserror'] , "submited": result["submited"]}, status=200)
                else:
                    return Response({"error":result['error']},status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                # if error raised
                return Response({"error":str(ex)},status=status.HTTP_400_BAD_REQUEST)
    # if challenge id is not provided
    return Response({"msg":"Challenge ID is required"},status=status.HTTP_400_BAD_REQUEST)