from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.utils.timezone import now, localtime

from django.utils import timezone
from rest_framework.views import APIView
from django.utils.timezone  import now
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Contest,ContestChallenge,ContestRegistration
from .serializers import ContestCreateSerializer, ContestEditSerializer , ContestChallengeSerializer , ContestListSerializer
from django.shortcuts import get_object_or_404, render

class ContestCreationView(APIView):
    permission_classes  = [IsAuthenticated]
    def get(self,req,contest_id):
        allContest = get_object_or_404(Contest,id=contest_id);
        serializeData = ContestEditSerializer(allContest)
        return Response(serializeData.data,status=status.HTTP_200_OK)

    def post(self,req):
        serializer = ContestCreateSerializer(data=req.data)
        if serializer.is_valid():
            contest = serializer.save(created_by  = req.user)
            return Response({"contest_id":contest.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, contest_id):
        """Contest Details Update"""
        print("contest id is" , contest_id)
        contest = Contest.objects.filter(id=contest_id, created_by=request.user).first()
        if not contest:
            return Response({"error": "Contest not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContestEditSerializer(contest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contest updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ContestChallengeManageView(APIView):
    permission_classes = [IsAuthenticated]
    # def get(self,request,contest_id):
    #     print(contest_id)  # ✅ Debugging ke liye print
    #     challenges_data = ContestChallenge.objects.filter(contest=contest_id).select_related('challenge')  
    #     if not challenges_data.exists():  # ✅ QuerySet ka `.exists()` use kar
    #         return Response({"error": "Contest not found or unauthorized"}, status=status.HTTP_400_BAD_REQUEST)
    #     # print(contestData)
    #     serializer = ContestChallengeSerializer(challenges_data, many=True)  # ✅ `many=True` add kar
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, contest_id):
        current_time = localtime(now())  # ✅ IST timezone me current time
        contest = get_object_or_404(Contest, id=contest_id)

        # ✅ Agar contest upcoming hai aur creator nahi hai toh access deny
        if contest.start_time > current_time and contest.created_by != request.user:
            return Response({"error": "Challenges are not available for upcoming contests"}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Contest live ya past hai, ya phir user creator hai toh challenges bhejo
        challenges_data = ContestChallenge.objects.filter(contest=contest).select_related('challenge')

        if not challenges_data.exists():
            return Response({"error": "No challenges found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContestChallengeSerializer(challenges_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, contest_id):
        """Add Challenge to Contest with Marks"""
        contest = Contest.objects.filter(id=contest_id, created_by=request.user).first()
        if not contest:
            return Response({"error": "Contest not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContestChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contest=contest)
            return Response({"message": "Challenge added to contest"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, contest_id, challenge_id):
        """Remove Challenge from Contest"""
        contest_challenge = ContestChallenge.objects.filter(contest__id=contest_id, challenge__id=challenge_id, contest__created_by=request.user).first()
        if not contest_challenge:
            return Response({"error": "Challenge not found in this contest"}, status=status.HTTP_404_NOT_FOUND)
        contest_challenge.delete()
        return Response({"message": "Challenge removed from contest"}, status=status.HTTP_200_OK)

class ContestListview(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        current_time = localtime(now())  # 👈 now converted to India timezone

        print("🕒 IST Time:", current_time)

        live_contests = Contest.objects.filter(
            start_time__lte=current_time,
            end_time__gt=current_time
        )

        upcoming_contests = Contest.objects.filter(
            start_time__gt=current_time
        )

        past_contests = Contest.objects.filter(
            end_time__lte=current_time
        )

        return Response({
            "live": ContestListSerializer(live_contests, many=True).data,
            "upcoming": ContestListSerializer(upcoming_contests, many=True).data,
            "past": ContestListSerializer(past_contests, many=True).data,
        }, status=status.HTTP_200_OK)

        

    

class ContestRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, contest_id):
        """Register user to a contest (only if upcoming)"""
        contest = get_object_or_404(Contest, id=contest_id)
        current_time = localtime(now())

        if contest.start_time <= current_time:
            return Response({"error": "You can only register for upcoming contests"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already registered
        if ContestRegistration.objects.filter(user=request.user, contest=contest).exists():
            return Response({"message": "Already registered"}, status=status.HTTP_200_OK)

        ContestRegistration.objects.create(user=request.user, contest=contest)
        return Response({"message": "Successfully registered"}, status=status.HTTP_201_CREATED)

    def delete(self, request, contest_id):
        """Unregister user from a contest"""
        contest = get_object_or_404(Contest, id=contest_id)
        registration = ContestRegistration.objects.filter(user=request.user, contest=contest).first()

        if not registration:
            return Response({"error": "You are not registered for this contest"}, status=status.HTTP_400_BAD_REQUEST)

        registration.delete()
        return Response({"message": "Successfully unregistered"}, status=status.HTTP_200_OK)

    def get(self, request, contest_id):
        """Check if user is registered"""
        contest = get_object_or_404(Contest, id=contest_id)
        is_registered = ContestRegistration.objects.filter(user=request.user, contest=contest).exists()
        return Response({"registered": is_registered}, status=status.HTTP_200_OK)





class ContestChallengeSubmissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, contest_id, challenge_id):
        user = request.user
        code = request.data.get("code")

        # Validate contest and challenge
        contest = get_object_or_404(Contest, id=contest_id)
        challenge = get_object_or_404(Challenges, id=challenge_id)

        if contest not in user.joined_contests.all():
            return Response({'detail': 'You are not registered for this contest.'}, status=status.HTTP_403_FORBIDDEN)

        # Fetch test cases


        
        submission = Submission.objects.create(
            user=user,
            contest=contest,
            challenge=challenge,
            code=code,
            status=final_status,
            score=total_score * 100,
        )

        if final_status == 'Accepted':
            update_leaderboard(submission)

        return Response({
            "status": final_status,
            "score": submission.score,
            "output": final_output if final_status == "Accepted" else "",
        }, status=status.HTTP_200_OK)


    def get(self, request, contest_id, challenge_id):
        """Get submissions for a challenge in a contest"""
        # Logic to retrieve submissions goes here
        return Response({"message": "Submissions retrieved successfully"}, status=status.HTTP_200_OK)
