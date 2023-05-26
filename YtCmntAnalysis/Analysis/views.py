from django.shortcuts import render, HttpResponse
import os
from django.core.cache import cache
import json
from django.apps import apps
from django.views import View
from .ML.sent_analysis import SimpleYtCommentAnalyzer
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
from .forms import YouTubeUrlForm
from googleapiclient.errors import HttpError


# Create your views here.
def test(request):
    """myapp_config = apps.get_app_config("Analysis")
    model = myapp_config.tweet_nlp_model
    print(type(model))
    obj = SimpleYtCommentAnalyzer(model, "QwreMeXlFoY")
    obj.get_comments_and_sentiment_by_video_id()
    temp = obj.get_summary()
    pretty_data = json.dumps(temp, indent=4)
    response = HttpResponse(content_type="text/plain")
    response.content = pretty_data
    return HttpResponse(response)"""
    return render(request, "sample_test.html")

def about(request):
    return render(request, "about.html")


class Analview(View):
    form_class = YouTubeUrlForm
    template_name = "index.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            video_comment_info = self.get_analysis(url)
            return JsonResponse(video_comment_info)
        return render(request, self.template_name, {"form": form})

    def get_analysis(self, url):
        url_id = self.get_yt_video_id(url)

        data = cache.get("yt_url_id_{}".format(url_id))
        if data is None:
            obj = SimpleYtCommentAnalyzer(url_id)
            try:
                obj.get_comments_and_sentiment_by_video_id()
                data = obj.get_summary()
                cache.set(
                    "yt_url_id_{}".format(url_id), data, 60 * 60 * 24 * 30
                )  # set cache time for 30 days
            except HttpError as e:
                if(e.error_details[0]["reason"]=="commentsDisabled"):
                    print("Comments are disabled")
                    data = {"Error": 403} #comments are disabled error code
                else:
                    print("Video not found")
                    data = {"Error": 404} # video not found error code
        # print(data)
        return data

    def get_yt_video_id(self, url):
        if url.startswith(("youtu", "www")):
            url = "http://" + url
        query = urlparse(url)
        if "youtube" in query.hostname:
            if query.path == "/watch":
                return parse_qs(query.query)["v"][0]
            elif query.path.startswith(("/embed/", "/v/")):
                return query.path.split("/")[2]
        elif "youtu.be" in query.hostname:
            return query.path[1:]
        else:
            raise ValueError
