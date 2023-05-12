from django.shortcuts import render,HttpResponse
import os
import json
import tweetnlp
from django.views import View
from .ML.sent_analysis import SimpleYtCommentAnalyzer
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
from .forms import YouTubeUrlForm

# Create your views here.
def test(request):
    model = tweetnlp.load_model('sentiment', multilingual=True)
    obj = SimpleYtCommentAnalyzer(model , "QwreMeXlFoY" )
    obj.get_comments_and_sentiment_by_video_id()
    temp=obj.get_summary()
    pretty_data = json.dumps(temp, indent=4)
    response = HttpResponse(content_type='text/plain')
    response.content = pretty_data
    return HttpResponse(response)

class Analview(View):
    form_class=YouTubeUrlForm
    template_name = 'index.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            video_comment_info = self.get_analysis(url)
            #print(video_comment_info)
            return JsonResponse(video_comment_info)
        return render(request, self.template_name, {'form': form})
    def get_analysis(self,url):
        url_id=self.get_yt_video_id(url)
        model = tweetnlp.load_model('sentiment', multilingual=True)
        obj = SimpleYtCommentAnalyzer(model,url_id)
        obj.get_comments_and_sentiment_by_video_id()
        temp=obj.get_summary()
        #print(temp)
        return temp
    def get_yt_video_id(self,url):
        if url.startswith(('youtu', 'www')):
            url = 'http://' + url
        query = urlparse(url)
        if 'youtube' in query.hostname:
            if query.path == '/watch':
                return parse_qs(query.query)['v'][0]
            elif query.path.startswith(('/embed/', '/v/')):
                return query.path.split('/')[2]
        elif 'youtu.be' in query.hostname:
            return query.path[1:]
        else:
            raise ValueError
