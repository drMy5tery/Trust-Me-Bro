from django.apps import AppConfig
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Analysis'
    def ready(self):
        # Code to execute at the start of the server
        #self.tweet_nlp_model = tweetnlp.load_model('sentiment', multilingual=True)
        self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        self.model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        print("Tweet NLP model loaded!")
    def get_tweet_nlp_model(self):
        return self.tweet_nlp_model
        