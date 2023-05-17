import os
import googleapiclient.discovery
import requests


class SimpleYtCommentAnalyzer:
    def __init__(self, video_id="DA7Dtu7eO3E"):
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.sentiment_summary = {}
        self.comments = []
        self.stats = {"title": "", "views": 0, "likes": 0, "commentcount": 0}

        self.top_five_positive_comments = {}
        self.top_five_negative_comments = {}
        self.top_five_comments = {}
        self.video_id = video_id
        self.API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
        self.headers = {"Authorization": "Bearer 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"}
        self.youtube = self.yt_api_build()

    def yt_api_build(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyBCLGapdQyFLEQNofdzYT0ZgRLrss0EeGw"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY
        )
        return youtube

    def get_info_about_video(self):
        request = self.youtube.videos().list(
            part="snippet,statistics", id=self.video_id
        )
        response = request.execute()
        self.stats["title"] = response["items"][0]["snippet"]["title"]
        self.stats["channel_name"] = response["items"][0]["snippet"]["channelTitle"]
        self.stats["thumbnail"] = response["items"][0]["snippet"]["thumbnails"][
            "standard"
        ]["url"]
        self.stats["views"] = response["items"][0]["statistics"]["viewCount"]
        self.stats["likes"] = response["items"][0]["statistics"]["likeCount"]
        self.stats["commentcount"] = response["items"][0]["statistics"]["commentCount"]

    def text_preprocessing(self, text):
        text.lower()
        data = text.split("\n")
        for val in data:
            val.strip()
        return " ".join(data)

    def query(self,text):
        payload = {
        "inputs": text,
        }
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        data = response.json()
        sorted_output = sorted(data[0], key=lambda d: d['score'], reverse=True)
        prediction = sorted_output[0]
        label_mapping = {
        'LABEL_0': 'negative',
        'LABEL_1': 'neutral',
        'LABEL_2': 'positive'
        }
        prediction['label'] = label_mapping[prediction['label']]
        return prediction
      
    def generate_score(self, text):
        score = TextBlob(text).sentiment.polarity
        if score == 0:
            label = "neutral"
        elif score > 0:
            label = "positive"
        else:
            label = "negative"
        return {"label": label, "score": score}

    def getAnalysis(self, label, text):
        score = label["label"]
        if score == "negative":
            self.top_five_negative_comments[text] = label["score"]
            self.negative += 1
            return "Negative"
        elif score == "neutral":
            self.neutral += 1
            return "Neutral"
        else:
            self.top_five_positive_comments[text] = label["score"]
            self.positive += 1
            return "Positive"

    def get_sentiment(self):
        if self.positive >= self.negative or self.neutral >= self.negative:
            self.top_five_comments = sorted(
                self.top_five_positive_comments.items(),
                key=lambda x: x[1],
                reverse=True,
            )
            return {
                "sentiment": "Valid",
                "Top_five_comments": self.top_five_comments[:5],
            }
        else:
            self.top_five_comments = sorted(
                self.top_five_negative_comments.items(),
                key=lambda x: x[1],
                reverse=True,
            )
            return {
                "sentiment": "InValid",
                "Top_five_comments": self.top_five_comments[:5],
            }

    def get_summary(self):
        self.get_info_about_video()
        self.stats.update(
            {
                "Sentiment_summary": self.sentiment_summary,
                "Scores": {
                    "positive": self.positive,
                    "negative": self.negative,
                    "neutral": self.neutral,
                },
            }
        )
        return self.stats

    def get_comments_and_sentiment_by_video_id(self):
        """ """
        nextPageToken = None
        total_comments = 0
        # positive , negative , neutral = 0 , 0 , 0

        while total_comments <= 5:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=self.video_id,
                maxResults=min(5, 5 - total_comments),
                pageToken=nextPageToken,
            )
            response = request.execute()

            for item in response["items"]:
                text = self.text_preprocessing(
                    item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                )
                sentiment = self.query(text)
         
                comment = {
                    "comment": text,
                    "comment_like": item["snippet"]["topLevelComment"]["snippet"][
                        "likeCount"
                    ],
                    "total_reply_Count": item["snippet"]["totalReplyCount"],
                    "sentiment": self.getAnalysis(sentiment,text),
                }

                self.comments.append(comment)
                total_comments += 1

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break
        self.sentiment_summary = self.get_sentiment()
