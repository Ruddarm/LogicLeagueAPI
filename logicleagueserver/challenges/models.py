from django.db import models
from users.models import LogicLeagueUser
import uuid

# Create your models here.

#Testcase 

    
#model Challenge model class
class Challenges(models.Model):
    challengeID= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name  = models.CharField(max_length=200,null=False)
    title = models.TextField(null=False)
    description = models.TextField(null=True)
    inputformat = models.TextField(null=True);
    outputformat = models.TextField(null=True)
    LEVEL_CHOICES = [("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),]
    tags = models.JSONField(null=True, blank=True)  
    level = models.CharField(max_length=10,choices=LEVEL_CHOICES,default="Easy")
    isPublic = models.BooleanField(default=True)
    createdBy = models.ForeignKey(LogicLeagueUser,on_delete=models.CASCADE,related_name="Challenges")
    def __str__(self):
        return self.name
class TestCase(models.Model):
    testCaseID = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    ifnput = models.TextField(null=False)
    output = models.TextField(null=False)
    desc =  models.TextField(null=True)
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