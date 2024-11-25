from django.db import models
from users.models import LogicLeagueUser
import uuid

# Create your models here.
class Challenges(models.Model):
    challengeID= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name  = models.CharField(max_length=200,null=False)
    title = models.TextField(null=False)
    description = models.TextField(null=True)
    inputformat = models.TextField(null=True);
    outputformat = models.TextField(null=True)
    tags = [models.CharField(max_length=150 , null=True)]
    LEVEL_CHOICES = [("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),]
    tags = models.JSONField(null=True, blank=True)  
    level = models.CharField(max_length=10,choices=LEVEL_CHOICES,default="Easy")
    isPublic = models.BooleanField(default=True)
    createdBy = models.ForeignKey(LogicLeagueUser,on_delete=models.CASCADE,related_name="Challenges")
    
    
    def __str__(self):
        return self.name
class Solution:
    pass
