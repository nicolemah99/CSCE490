from django.urls import path
from . import views

app_name = "baseball"
urlpatterns = [
    path("", views.index, name="index"),
    path("standings", views.standings, name="standings"),
    path('logos', views.logos, name="logos"),    
    path('redsox', views.redsox, name="redsox"),
    path('oneteam/<str:code>', views.oneteam, name="oneteam"),
]
