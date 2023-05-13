import os
import googleapiclient.discovery
from vaderSentiment.vaderSentiment  import SentimentIntensityAnalyzer


class SimpleYtCommentAnalyzer:
    def __init__(self,model, video_id = "DA7Dtu7eO3E"):
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.sentiment_summary = {}
        self.comments = []
        self.stats = {
            "title" : "",
            "views" : 0,
            "likes" : 0,
            "commentcount" :0  
            }

        self.top_five_comments = {}

        self.video_id = video_id
        self.model = model
        self.youtube = self.yt_api_build()
        self.sid_obj = SentimentIntensityAnalyzer()

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
        self.stats["like_view_ratio"]=float(int( self.stats['likes'])/int(self.stats['views']))
        self.stats["comment_view_ratio"]=float(int( self.stats['commentcount'])/int(self.stats['views']))
    def text_preprocessing(self,text):
        text.lower()
        data = text.split("\n")
        for val in data:
            val.strip()
        return " ".join(data)

    def getAnalysis(self,label,text):
        score = label['label']
        if score == 'negative':
            self.top_five_comments[text] = label['probability'][score]
            self.negative += 1
            return 'Negative'
        elif score == 'netural':
            self.neutral += 1
            return 'Neutral'
        else:
            self.top_five_comments[text] = label['probability'][score]
            self.positive += 1
            return 'Positive'

    def get_sentiment(self):
        if ((self.positive >= self.negative or  self.neutral >= self.negative)):
            self.top_five_comments = sorted( self.top_five_comments.items(), key=lambda x:x[1],reverse=True)
            return { "sentiment" :"Valid" , "Top_five_comments" : self.top_five_comments[:5] }
        else:
            self.top_five_comments = sorted( self.top_five_comments.items(), key=lambda x:x[1],reverse=True)
            return { "sentiment" :"InValid" , "Top_five_comments" : self.top_five_comments[:5] }
    
    def get_summary(self):
        self.get_info_about_video()
        self.stats.update(
            {
            "Sentiment_summary" : self.sentiment_summary,
            "Scores" : {
                "positive" : self.positive,
                "negative" : self.negative,
                "neutral" : self.neutral
                
                }
            }
        )
        return self.stats
    
    def get_comments_and_sentiment_by_video_id(self):
        """
        """
        nextPageToken = None
        total_comments=0
        #positive , negative , neutral = 0 , 0 , 0

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
                            "sentiment" : self.getAnalysis(self.model.sentiment(text, return_probability=True),text)
                }

                self.comments.append(comment)
                total_comments+=1

            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break
        self.sentiment_summary = self.get_sentiment()
        

