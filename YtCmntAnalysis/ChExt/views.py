from django.shortcuts import render
from Analysis.views import Analview
from django.http import JsonResponse
# Create your views here.

class Cext(Analview):
    template_name="chrome_ext.html"
    

