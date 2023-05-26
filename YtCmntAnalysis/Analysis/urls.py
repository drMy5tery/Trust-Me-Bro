from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='test'),
    path('about/', views.about, name='about'),
    path('analysis/',views.Analview.as_view(), name='analysis'),
    
]
