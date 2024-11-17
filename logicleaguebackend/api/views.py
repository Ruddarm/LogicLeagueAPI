from django.shortcuts import render
from django.http import HttpResponse;
# Create your views here#
#HOme page
def home_Page(req):
    print("On home page")
    return HttpResponse("fucking home page")