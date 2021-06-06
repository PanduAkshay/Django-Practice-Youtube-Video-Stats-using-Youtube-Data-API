from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from youtubesearchpython import Video as YVideo
from datetime import timedelta, datetime
from firstApp.forms import VideoForm
from firstApp.models import Video
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from firstApp.youtubeAPIConfig import youtube


@login_required
def home(request, pk=None):
    if request.method == "POST":
        get_video_form = VideoForm(request.POST)
        if get_video_form.is_valid():
            object = get_video_form.save(user=request.user)
            return redirect('app-home', pk=object.id)
    else:
        get_video_form = VideoForm()
        temp = Video.objects.filter(id=pk).first()
        video = None
        if temp:
            video_data = YVideo.get(temp.videoLink)
            if video_data:
                video = {}
                video['id'] = video_data['id']
                video['title'] = video_data['title']
                video['thumbnail'] = video_data['thumbnails'][0]['url']
                # video['description'] = repr(video_data['description'])
                video['channel_name'] = video_data['channel']['name']
                video['channel_link'] = video_data['channel']['link']
                video['rating'] = video_data['averageRating']
                video['keywords'] = video_data['keywords']
                video['upload_date'] = video_data['uploadDate']
                video['url'] = video_data['link']

                duration = int(video_data['streamingData']['formats'][0]['approxDurationMs'].strip('ms'))//1000
                video['duration'] = {}
                video['duration']['hours'], video['duration']['minutes'], video['duration']['seconds'] = str(timedelta(seconds=duration)).split(':')

                video['viewCount'] = video_data['viewCount']['text'] 
                

    return render(request, 'firstApp/home.html', {"get_video_form":get_video_form, 'video':video})

def getVideoStats(request, id):
    video_request = youtube.videos().list(
        part = "statistics",
        id = id
    )
    video_Stats = video_request.execute()
    stats = {
        'like_count': int(video_Stats['items'][0]['statistics']['likeCount']) ,
        'dislike_count': int(video_Stats['items'][0]['statistics']['dislikeCount']),
        'comment_count': int(video_Stats['items'][0]['statistics']['commentCount']),
        'label': datetime.now().strftime("%H:%M:%S")
    }
    return JsonResponse(stats)



class HistoryView( LoginRequiredMixin ,ListView):
    model = Video
    def get_queryset(self):
        return self.request.user.video_set.order_by("-atdatetime").all()

@login_required
def clearHistory(request):
    request.user.video_set.all().delete()
    messages.success(request,'History Cleared...')
    return redirect('app-history')

