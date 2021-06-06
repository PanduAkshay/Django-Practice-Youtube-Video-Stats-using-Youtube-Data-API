from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    videoLink = models.CharField(max_length = 200)
    atdatetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE )
