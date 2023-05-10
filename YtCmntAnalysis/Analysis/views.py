from django.shortcuts import render,HttpResponse
import os
import json
from .ML.sent_analysis import SimpleYtCommentAnalyzer

# Create your views here.
def test(request):
    obj = SimpleYtCommentAnalyzer("QwreMeXlFoY")
    obj.get_comments_and_sentiment_by_video_id()
    temp=obj.get_summary()
    pretty_data = json.dumps(temp, indent=4)
    response = HttpResponse(content_type='text/plain')
    response.content = pretty_data
    return HttpResponse(response)