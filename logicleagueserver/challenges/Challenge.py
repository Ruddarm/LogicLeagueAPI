

from .serializers import CreateChallengeSerializer
from rest_framework.response import Response
from rest_framework import status

def create_challenge(logic_league_user,challenge_data):
        serializer = CreateChallengeSerializer(data=challenge_data)
        if serializer.is_valid():
            new_challenge =  serializer.create(serializer.data,logic_league_user)
            return new_challenge.challengeID;
        else:
            return Response({ "msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
def get_challenge():
    pass