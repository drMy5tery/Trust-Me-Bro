import os
import googleapiclient.discovery
from textblob import TextBlob
import requests


class SimpleYtCommentAnalyzer:
    def __init__(self, video_id="DA7Dtu7eO3E"):
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.sentiment_summary = {}
        self.comments = []
        self.comment_count = 0
        self.max_size = 512
        self.stats = {"title": "", "views": 0, "likes": 0, "commentcount": 0}

        self.top_five_positive_comments = {}
        self.top_five_negative_comments = {}
        self.top_five_comments = {}
        self.video_id = video_id
        self.youtube = self.yt_api_build()

    def yt_api_build(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = str(os.environ.get("YOUTUBE_API"))
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY
        )
        return youtube

    def query(self, payload):
        API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
        headers = {"Authorization": "Bearer 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"}
        label_mapping = {
            "LABEL_0": "negative",
            "LABEL_1": "neutral",
            "LABEL_2": "positive",
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        response = response.json()

        if "error" in response:
            print(response)
            return "False"

        for index, (data, comment) in enumerate(zip(response, self.comments)):
            sorted_output = sorted(data, key=lambda d: d["score"], reverse=True)
            prediction = sorted_output[0]
            prediction["label"] = label_mapping[prediction["label"]]
            comment["sentiment"] = self.getAnalysis(prediction, comment["comment"])
            self.comments[index] = comment

        return True

    def get_info_about_video(self):
        request = self.youtube.videos().list(
            part="snippet,statistics", id=self.video_id
        )
        response = request.execute()
        assert len(response["items"]) != 0, "Invalid video Id"

        self.comment_count = int(
            response["items"][0]["statistics"].get("commentCount", False)
        )
        if not self.comment_count:
            raise Exception("commentsDisabled")

        try:
            if self.comment_count < 500:
                self.stats[
                    "Error"
                ] = 500  # This error code indicates comments below 500
            self.stats["title"] = response["items"][0]["snippet"]["title"]
            self.stats["channel_name"] = response["items"][0]["snippet"]["channelTitle"]
            self.stats["thumbnail"] = response["items"][0]["snippet"]["thumbnails"][
                "high"
            ]["url"]

        except KeyError:
            self.stats["thumbnail"] = response["items"][0]["snippet"]["thumbnails"][
                "standard"
            ]["url"]
        finally:
            self.stats["views"] = self.format_number_with_suffix(
                int(response["items"][0]["statistics"]["viewCount"])
            )
            self.stats["likes"] = self.format_number_with_suffix(
                int(response["items"][0]["statistics"].get("likeCount", 0))
            )
            self.stats["commentcount"] = self.format_number_with_suffix(
                self.comment_count
            )

    def text_preprocessing(self, text):
        text.lower()
        data = text.split("\n")
        for val in data:
            val.strip()
        return " ".join(data)

    def format_number_with_suffix(self, number):
        suffixes = [
            "",
            "k",
            "m",
            "b",
            "t",
        ]  # List of suffixes for thousands, millions, billions, trillion
        magnitude = 0

        while abs(number) >= 1000:
            number /= 1000.0
            magnitude += 1

        return f"{number:.1f}{suffixes[magnitude]}"

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
        if self.positive >= self.negative or (self.neutral >= self.negative and self.positive >= self.negative):
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

        if self.comment_count >= 500:
            data = self.get_comments_and_sentiment_by_video_id()
            if data:
                self.stats.update(
                    {
                        "video_analysis": {
                            "Sentiment_summary": self.sentiment_summary,
                            "Scores": {
                                "positive": self.positive,
                                "negative": self.negative,
                                "neutral": self.neutral,
                            },
                        }
                    }
                )
            else:
                self.stats["Error"] = 504

        return self.stats

    def get_comments_and_sentiment_by_video_id(self):
        """ """
        nextPageToken = None
        total_comments = 0
        comments = []
        # positive , negative , neutral = 0 , 0 , 0

        while total_comments <= 500:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=self.video_id,
                maxResults=min(100, 500 - total_comments),
                pageToken=nextPageToken,
            )
            response = request.execute()

            for item in response["items"]:
                text = self.text_preprocessing(
                    item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                )
                text = text[: self.max_size]
                comments.append(text)

                comment = {
                    "comment": text,
                    "comment_like": item["snippet"]["topLevelComment"]["snippet"][
                        "likeCount"
                    ],
                    "total_reply_Count": item["snippet"]["totalReplyCount"],
                }

                self.comments.append(comment)
                total_comments += 1

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break

        resp = self.query(comments)
        if resp:
            self.sentiment_summary = self.get_sentiment()
            return True
        else:
            return False
