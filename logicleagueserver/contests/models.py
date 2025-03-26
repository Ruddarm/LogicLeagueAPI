from django.db import models
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


from challenges.models import Challenges
#from users.models import UserManager

from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User

class Contest(models.Model):
    # Unique ID
    id = models.AutoField(primary_key=True)

    # details
    name = models.CharField(max_length=255, null=False, blank=False) 
    description = models.TextField(null=False, blank=False)
    start_time = models.DateTimeField(null=False, blank=False, default=timezone.now)
    end_time = models.DateTimeField(null=False, blank=False, default=timezone.now) 
    prizes = models.TextField(max_length=300, blank=True, null=True) 

    # Status
    is_public = models.BooleanField(default=False) 

    #challenge = models.ForeignKey(Challenges, on_delete=models.CASCADE, related_name='contests')

    # Array of participants
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contests', blank=True)

    def __str__(self):
        return self.name
    
    '''@property
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time'''



'''
    # uui contest id - done
    # defuult value , not null validaiton - done
    # prizes, - done
    # isactve, is public ,  - done
    # challegne foreign key .challemnge models
    name = models.CharField(max_length=255, null= False)
    description = models.TextField(null= False)
    start_time = models.DateTimeField(null= False, default= timezone.now)
    end_time = models.DateTimeField(null= False, default=timezone.now)
    prizes = models.CharField(max_length=300)
    # array of user id '''
    
# constest -reg model

@login_required
def register_for_contest(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)

    if contest.is_active and contest.start_time > timezone.now():
        contest.participants.add(request.user)
        messages.success(request, f"You have successfully registered for the contest: {contest.name}.")
    else:
        messages.error(request, "Registration is closed or the contest has already started.")

    return redirect('contest_detail', contest_id=contest.id) 
# contest Id , user Id 

class Problem(models.Model):
    contest = models.ForeignKey(Contest, related_name='problems', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    constraints = models.TextField()
    test_cases = models.JSONField()  # Use a JSON field to store test cases

    def __str__(self):
        return self.title
# almost ok hia 
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
