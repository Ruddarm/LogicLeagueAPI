from django.shortcuts import render
from rest_framework.permissions import AllowAny

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Contest,ContestChallenge
from .serializers import ContestCreateSerializer, ContestEditSerializer , ContestChallengeSerializer
from django.shortcuts import get_object_or_404, render

class ContestCreationView(APIView):
    permission_classes  = [IsAuthenticated]
    def post(self,req):
        serializer = ContestCreateSerializer(data=req.data)
        if serializer.is_valid():
            contest = serializer.save(created_by  = req.user)
            return Response({"contest_id":contest.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, contest_id):
        """Contest Details Update"""
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
