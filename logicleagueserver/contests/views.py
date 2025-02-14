from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Contest, Problem
from .serializers import ContestSerializer, ProblemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from challenges.models import Challenges  # Import the Challenges model
from uuid import UUID



# Helper function to validate challenge IDs
def validate_challenge_ids(challenge_ids):
    if not isinstance(challenge_ids, list):
        return False, "Challenges must be provided as a list of IDs."
    if not all(isinstance(id, int) for id in challenge_ids):
        return False, "All challenge IDs must be integers."
    return True, None

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def contest_list(request):
    """List active and upcoming contests."""
    current_time = timezone.now()

    # Get active contests (current time is between start_time and end_time)
    active_contests = Contest.objects.filter(start_time__lte=current_time, end_time__gte=current_time)
    
    # Get upcoming contests (contests that haven't started yet)
    upcoming_contests = Contest.objects.filter(start_time__gt=current_time)

    # Serialize the contests
    active_serializer = ContestSerializer(active_contests, many=True)
    upcoming_serializer = ContestSerializer(upcoming_contests, many=True)

    return Response({
        "active_contests": active_serializer.data,
        "upcoming_contests": upcoming_serializer.data,
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def contest_registration(request, contest_id):
    """Register a user for a contest."""
    try:
        contest = Contest.objects.get(id=contest_id)
    except Contest.DoesNotExist:
        return Response({"error": "Contest not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Check if the user is already registered for this contest
    if user in contest.participants.all():
        return Response({"message": "User already registered"}, status=status.HTTP_400_BAD_REQUEST)

    # Add the user to the participants list
    contest.participants.add(user)
    contest.save()

    return Response({"message": "User registered successfully for the contest"}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def contest_detail(request, contest_id):
    """Get details of a specific contest."""
    contest = get_object_or_404(Contest, id=contest_id)
    serializer = ContestSerializer(contest)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def contest_admin_list(request):
    """List all contests or create a new contest."""
    if request.method == 'GET':
        contests = Contest.objects.all()
        serializer = ContestSerializer(contests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create contest without challenges
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([AllowAny])
def contest_admin_manage(request):
    """List all contests, create a new contest, or delete an existing contest."""
    if request.method == 'GET':
        current_time = timezone.now()

        # Filter contests based on time
        contests = Contest.objects.filter(start_time__lte=current_time, end_time__gte=current_time) | Contest.objects.filter(start_time__gte=current_time)

        serializer = ContestSerializer(contests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a contest without challenges initially
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contest_id = request.data.get("contest_id", None)
        if not contest_id:
            return Response({"error": "Contest ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        contest = get_object_or_404(Contest, id=contest_id)
        contest.delete()
        return Response({"message": "Contest deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def contest_admin_detail(request, contest_id):
    """Retrieve, update, or delete a specific contest."""
    contest = get_object_or_404(Contest, id=contest_id)

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

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def add_challenges_to_contest(request, contest_id):
    try:
        # Retrieve contest instance
        contest = Contest.objects.get(id=contest_id)

        # Get 'challenges' from request data and validate it
        challenge_uuids = request.data.get("challenges", [])
        if not isinstance(challenge_uuids, list) or not challenge_uuids:
            return Response(
                {"error": "Invalid or missing 'challenges' field. Provide a list of challenge IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter challenges using the IDs provided
        challenges = Challenges.objects.filter(challengeID__in=challenge_uuids)
        if not challenges.exists():
            return Response(
                {"error": "No valid challenges found with the provided IDs."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Add challenges to the contest
        contest.challenges.add(*challenges)
        return Response(
            {"message": "Challenges added to the contest successfully."},
            status=status.HTTP_200_OK
        )
    except Contest.DoesNotExist:
        return Response(
            {"error": "Contest not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def play_contest(request, contest_id):
    """Play challenges in a contest sequentially."""
    contest = get_object_or_404(Contest, id=contest_id)
    current_time = timezone.now()

    # Check if the contest is active
    if not (contest.start_time <= current_time <= contest.end_time):
        return Response({"error": "The contest is not active"}, status=status.HTTP_400_BAD_REQUEST)

    # Get challenges in the order they were added
    challenges = contest.challenges.order_by('id')
    serializer = ProblemSerializer(challenges, many=True)

    return Response({
        "contest": ContestSerializer(contest).data,
        "challenges": serializer.data,
    }, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_contest(request, contest_id):
    """Delete a specific contest."""
    contest = get_object_or_404(Contest, id=contest_id)
    contest.delete()
    return Response({"message": "Contest deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
