from django.shortcuts import render
from django.core.cache import cache
from django.apps import apps
from django.views import View
from .ML.sent_analysis import SimpleYtCommentAnalyzer
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
from .forms import YouTubeUrlForm


def about(request):
    return render(request, "about.html")


class Analview(View):
    form_class = YouTubeUrlForm
    template_name = "index.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        url = request.POST.get("url")
        video_comment_info = self.get_analysis(url)
        return JsonResponse(video_comment_info)

    def get_analysis(self, url):
        url_id = self.get_yt_video_id(url)

        data = cache.get("yt_url_id_{}".format(url_id))
        if data is None:
            obj = SimpleYtCommentAnalyzer(url_id)
            try:
                data = obj.get_summary()
                cache.set(
                    "yt_url_id_{}".format(url_id), data, 60 * 60 * 24 * 30
                )  # set cache time for 30 days
            except AssertionError as e:
                if str(e) == "Invalid video Id":
                    print("Video not found")
                    data = {"Error": 404}  # video not found error code
            except Exception as e:
                if str(e) == "commentsDisabled":
                    print("Comments are disabled")
                    data = {"Error": 403}  # comments are disabled error code
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
