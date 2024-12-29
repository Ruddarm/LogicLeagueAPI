from django.db import models
from users.models import LogicLeagueUser
import uuid

# Create your models here.

#Testcase 

    
#model Challenge model class
class Challenges(models.Model):
    challengeID= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challengeName  = models.CharField(max_length=200,null=False)
    challengeDesc = models.TextField(null=True)
    problemStatement = models.TextField(null=False)
    
    inputFormat = models.TextField(null=True);
    outputFormat = models.TextField(null=True)
    constraints = models.TextField(null=True)
    LEVEL_CHOICES = [("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),]
    tags = models.JSONField(null=True, blank=True)  
    challengeLevel = models.CharField(max_length=10,choices=LEVEL_CHOICES,default="Easy")
    isPublic = models.BooleanField(default=True)
    createdBy = models.ForeignKey(LogicLeagueUser,on_delete=models.CASCADE,related_name="Challenges")
    # def __str__(self):
    #     return self.name
class TestCase(models.Model):
    testCaseID = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    # variables = models.TextField(null=False , default="");
    # values = models.TextField(null=False ,default="")
    input = models.JSONField(null=False, default=dict)
    input_txt = models.TextField(null=False ,default="")
    output = models.TextField(null=False , default="")
    output_txt = models.TextField(null=False, default="")
    explaination =  models.TextField(null=True,default="")
    isSample = models.BooleanField(default=True)
    marks = models.SmallIntegerField(default=0)
    challengeID = models.ForeignKey(Challenges,on_delete=models.CASCADE)    

class Solution(models.Model):
    solutionID= models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    language = models.CharField(max_length=100,null=False)
    code = models.TextField(null=True,default="");
    submission_date_time = models.DateTimeField
    runtime = models.CharField(null=True)
    space = models.CharField(null=True)
    challengeID = models.ForeignKey(Challenges,on_delete=models.CASCADE)
    submitedBy = models.ForeignKey(LogicLeagueUser,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    
