from django.shortcuts import render
from rest_framework.permissions import AllowAny

from django.utils import timezone

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Contest
from .serializers import ContestSerializer
from django.shortcuts import get_object_or_404, render

@api_view(['GET'])
@permission_classes([AllowAny])
def contest_list(request):
    if request.method == 'GET':
        current_time = timezone.now()

        # Get active contests (current time is between start_time and end_time)
        active_contests = Contest.objects.filter()
        
        # Get upcoming contests (contests that haven't started yet)
        upcoming_contests = Contest.objects.filter(start_time__gte=current_time)
        # past_contests = Contest.objects.filter(start_)
        # Serialize the contests
        active_serializer = ContestSerializer(active_contests, many=True)
        upcoming_serializer = ContestSerializer(upcoming_contests, many=True)

        return Response({
            "active_contests": active_serializer.data,
            "upcoming_contests": upcoming_serializer.data,
        })

def contest_detail(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)
    is_registered = request.user in contest.participants.all() if request.user.is_authenticated else False

    context = {
        'contest': contest,
        'is_registered': is_registered,
    }
    return render(request, 'contest_detail.html', context)

# get details of a contest
'''
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def contest_list(request):
    if request.method == 'GET':
        contests = Contest.objects.all()
        serializer = ContestSerializer(contests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''



@api_view(['POST'])
@permission_classes([AllowAny])  # Or use a more restrictive permission class
def contest_registration(request, contest_id):
    try:
        contest = Contest.objects.get(id=contest_id)
    except Contest.DoesNotExist:
        return Response({"error": "Contest not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user  # Ensure the user is authenticated
    if user in contest.participants.all():
        return Response({"message": "User already registered"}, status=status.HTTP_400_BAD_REQUEST)

    contest.participants.add(user)
    contest.save()
    return Response({"message": "User registered successfully"}, status=status.HTTP_200_OK)


'''# Admin view for managing contests
@api_view(['GET', 'POST'])
def contest_admin_list(request):
    #if not request.user.is_staff:
        #return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        try:
            contests = Contest.objects.all()  # Fetch all contests (admin view)
            return Response(contests)  # Return contests in the response
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    elif request.method == 'POST':
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
        
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def contest_admin_list(request):
    if request.method == 'GET':
        contests = Contest.objects.all()
        serializer = ContestSerializer(contests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def contest_admin_manage(request):
    if request.method == 'GET':
        contests = Contest.objects.filter(active=True) | Contest.objects.filter(start_time__gte=now())
        serializer = ContestSerializer(contests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def contest_admin_detail(request, contest_id):
    # Uncomment the staff check if needed
    # if not request.user.is_staff:
    #     return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        contest = Contest.objects.get(id=contest_id)
    except Contest.DoesNotExist:
        return Response({"error": "Contest not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        try:
            serializer = ContestSerializer(contest)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"Serialization error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        try:
            serializer = ContestSerializer(contest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Update error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        try:
            contest.delete()
            return Response({"message": "Contest deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Delete error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Admin view for a single contest
'''@api_view(['GET', 'PUT', 'DELETE'])
def contest_admin_detail(request, contest_id):
    #if not request.user.is_staff:
        #return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        contest = Contest.objects.get(id=contest_id)
    except Contest.DoesNotExist:
        return Response({"error": "Contest not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContestSerializer(contest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContestSerializer(contest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contest.delete()
        return Response({"message": "Contest deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
'''




'''
@api_view
class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
'''