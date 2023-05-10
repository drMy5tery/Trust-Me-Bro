import os
import pprint
import nltk
import googleapiclient.discovery
nltk.download("vader_lexicon")
from nltk.sentiment.vader  import SentimentIntensityAnalyzer


class SimpleYtCommentAnalyzer:
    def __init__(self,video_id = "DA7Dtu7eO3E"):
        self.postive = 0
        self.negative = 0
        self.netural = 0
        self.sentiment = ""
        self.comments = []
        self.stats = {
            "title" : "",
            "views" : 0,
            "likes" : 0,
            "commentcount" :0,
            "like:view ratio": 0.0,  
            "comment:view ratio": 0.0,
        }
        self.video_id = video_id
        self.youtube = self.yt_api_build()
        self.sid= SentimentIntensityAnalyzer()

    def yt_api_build(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyBCLGapdQyFLEQNofdzYT0ZgRLrss0EeGw"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)
        return youtube

    def get_info_about_video(self):
        request = self.youtube.videos().list(
        part="snippet,statistics",
        id=self.video_id
        )
        response = request.execute()
        self.stats['title'] = response['items'][0]['snippet']['title']
        self.stats['views'] = response['items'][0]['statistics']['viewCount']
        self.stats['likes'] = response['items'][0]['statistics']['likeCount']
        self.stats['commentcount'] = response['items'][0]['statistics']['commentCount']
        self.stats["like:view ratio"]=float(int( self.stats['likes'])/int(self.stats['views']))
        self.stats["comment:view ratio"]=float(int( self.stats['commentcount'])/int(self.stats['views']))
    def text_preprocessing(self,text):
        text.lower()
        data = text.split("\n")
        for val in data:
            val.strip()
        return " ".join(data)

    def getAnalysis(self,score):
        score=score['compound']
        if score < 0:
            self.negative += 1
            return 'Negative'
        elif score == 0:
            self.netural += 1
            return 'Neutral'
        else:
            self.postive += 1
            return 'Positive'
    
    def get_sentiment(self):
        if ((self.postive >= self.netural and self.postive >= self.negative) or (self.netural >= self.postive and self.postive >= self.negative)):
            return "Valid"
        else:
            return "InValid"
    
    def get_summary(self):
        self.get_info_about_video()
        self.stats.update(
            {
            "Sentiment" : self.sentiment,
            "Scores" : {
                "postive" : self.postive,
                "negative" : self.negative,
                "netural" : self.netural
                
                }
            }
        )
        return self.stats

    def get_comments_and_sentiment_by_video_id(self):
        """
        """
        nextPageToken = None
        total_comments=0
        #postive , negative , netural = 0 , 0 , 0

        while total_comments<=500:
            request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=self.video_id,
                maxResults=min(100, 500 - total_comments),
                pageToken=nextPageToken
            )
            response = request.execute()

            for item in response['items']:
                text = self.text_preprocessing(item['snippet']['topLevelComment']['snippet']['textOriginal'])
                comment = {
                            "comment" : text,
                            "comment_like" : item['snippet']['topLevelComment']['snippet']['likeCount'],
                            "total_reply_Count" : item['snippet']['totalReplyCount'],
                            "sentiment" : self.getAnalysis(self.sid.polarity_scores(text))
                }

                self.comments.append(comment)
                total_comments+=1

            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                self.sentiment = self.get_sentiment()
            return self.comments , self.sentiment

        self.sentiment = self.get_sentiment()
        print(self.sentiment)
        return self.comments,self.sentiment

