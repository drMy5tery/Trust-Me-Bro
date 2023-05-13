from django.apps import AppConfig
import tweetnlp

class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Analysis'
    def ready(self):
        # Code to execute at the start of the server
        self.tweet_nlp_model = tweetnlp.load_model('sentiment', multilingual=True)
        print("Tweet NLP model loaded!")
    #def get_tweet_nlp_model(self):
        #return self.tweet_nlp_model
