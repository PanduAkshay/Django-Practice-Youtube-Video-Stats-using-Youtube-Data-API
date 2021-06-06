from django.urls import path
from firstApp.views import HistoryView
from firstApp import views

urlpatterns = [
    path('home/<int:pk>', views.home, name="app-home"),
    path('home/', views.home, name="app-home"),
    path('', views.home, name="app-home"),
    path('history/', HistoryView.as_view() , name="app-history"),
    path('stats/<id>', views.getVideoStats , name="app-video-stats"),
    path('clearHistory/', views.clearHistory , name = "app-clear-history" ),

]