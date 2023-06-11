from django.apps import AppConfig
class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Analysis'
    def ready(self):
        # Code to execute at the start of the server
        print("Default text blob NLP model loaded!")