from django.shortcuts import render
from Analysis.views import Analview
from django.http import JsonResponse
# Create your views here.

class Cext(Analview):
    yt_url=""
    def get(self, request):
       self.yt_url=request.GET['url']
       video_comment_info = self.get_analysis(self.yt_url)
       return JsonResponse(video_comment_info)

