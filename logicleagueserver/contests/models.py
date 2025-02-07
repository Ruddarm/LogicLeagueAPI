
from django.db import models
from django.utils import timezone
from django.conf import settings
from challenges.models import Challenges

class Contest(models.Model):
    # Unique ID
    id = models.AutoField(primary_key=True)

    # details
    name = models.CharField(max_length=255, null=False, blank=False) 
    description = models.TextField(null=False, blank=False)
    start_time = models.DateTimeField(null=False, blank=False, default=timezone.now)
    end_time = models.DateTimeField(null=False, blank=False, default=timezone.now) 
    prizes = models.CharField(max_length=300, blank=True, null=True) 

    # Status
    is_public = models.BooleanField(default=False) 

    # Array of participants
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contests', blank=True)

    # Relationship with Challenges
    challenges = models.ManyToManyField(Challenges, related_name='contests', blank=True)

    def __str__(self):
        return self.name

class Problem(models.Model):
    contest = models.ForeignKey(Contest, related_name='contest_problems', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    constraints = models.TextField()
    test_cases = models.JSONField()  # Use a JSON field to store test cases

    def __str__(self):
        return self.title

class Submission(models.Model):
    problem = models.ForeignKey(Problem, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submissions', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(max_length=50)  # e.g., "Accepted", "Wrong Answer"
    execution_time = models.FloatField()
    score = models.IntegerField()

    def __str__(self):
        return f"Submission by {self.user} for {self.problem}"