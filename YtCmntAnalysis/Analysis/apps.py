from django.apps import AppConfig
class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Analysis'
    def ready(self):
        # Code to execute at the start of the server
        #self.tweet_nlp_model = tweetnlp.load_model('sentiment', multilingual=True)
        # self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        # self.model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        print("Default text blob NLP model loaded!")