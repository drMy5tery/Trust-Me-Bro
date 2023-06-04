from django.urls import path
from . import views

urlpatterns = [
    path('',views.Cext.as_view(), name='c_ext'),
    
]
