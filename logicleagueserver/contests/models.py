from django.db import models
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from challenges.models import Challenges
#from users.models import UserManager
from django.db import models
from django.utils import timezone
import uuid
from users.models import LogicLeagueUser
#from django.contrib.auth.models import User

class Contest(models.Model):
    # Unique ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Details
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)  # Default hata diya, user set karega
    prizes = models.TextField(blank=True, null=True)
    
    # Status
    is_public = models.BooleanField(default=True)

    # Relationships
    created_by = models.ForeignKey(
        LogicLeagueUser, 
        on_delete=models.CASCADE, 
        null=True,
        related_name="created_contests"  # 👈 Better naming
    )

    participants = models.ManyToManyField(
        LogicLeagueUser, 
        related_name="joined_contests",  # 👈 Better naming
        blank=True
    )

    challenges = models.ManyToManyField(
        Challenges, 
        related_name="contests"  # 👈 Plural form rakha
    )

    def __str__(self):
        return self.name
    

class ContestChallenge(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="contest_challenges")
    challenge = models.ForeignKey(Challenges, on_delete=models.CASCADE , null=True)
    marks = models.IntegerField(default=0)  # Challenge ke marks
    
    class Meta:
        unique_together = ('contest', 'challenge')  # Ek contest me ek challenge sirf ek baar ho sakta hai

    def __str__(self):
        return f"{self.contest.name} - {self.challenge.title} ({self.marks} Marks)"

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(LogicLeagueUser, on_delete=models.CASCADE, related_name="submissions")
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="submissions" , null=True)
    challenge = models.ForeignKey(Challenges, on_delete=models.CASCADE, related_name="submissions", null=True, blank=True)
    code = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('Accepted', 'Accepted'), 
        ('Wrong Answer', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'), 
        ('Compilation Error', 'Compilation Error')
    ], default='Compilation Error')
    execution_time = models.FloatField(null=True, blank=True)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True , null=True)
class ContestLeaderboard(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="leaderboard")
    user = models.ForeignKey(LogicLeagueUser, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    last_submission_time = models.DateTimeField(null=True, blank=True)  # 👈 Track karega ki user ne last submission kab kiya

    class Meta:
        unique_together = ('contest', 'user')  # Har user ek contest me ek hi bar store hoga

    def __str__(self):
        return f"{self.user.username} - Score: {self.total_score}, Last Submit: {self.last_submission_time}"


def get_sorted_leaderboard(contest):
    return ContestLeaderboard.objects.filter(contest=contest).order_by('-total_score', 'last_submission_time')

def update_leaderboard(submission):
    leaderboard_entry, created = ContestLeaderboard.objects.get_or_create(
        contest=submission.contest, user=submission.user
    )
    # Best score leke update karna
    leaderboard_entry.total_score = max(leaderboard_entry.total_score, submission.score)
    leaderboard_entry.last_submission_time = submission.submitted_at
    leaderboard_entry.save()
