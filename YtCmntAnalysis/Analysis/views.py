from django.shortcuts import render,HttpResponse
import os

import googleapiclient.discovery

# Create your views here.
def test(request):
     # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBCLGapdQyFLEQNofdzYT0ZgRLrss0EeGw"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    video_id = "yoFvVAMcwOE"  # Replace with your desired video ID

    # Retrieve the video's comments
    comments = []
    nextPageToken = None
    total_comments=0

    while total_comments<=500:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(100, 500 - total_comments),
            pageToken=nextPageToken
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
            total_comments+=1

        nextPageToken = response.get('nextPageToken')


    return HttpResponse(i for i in comments)