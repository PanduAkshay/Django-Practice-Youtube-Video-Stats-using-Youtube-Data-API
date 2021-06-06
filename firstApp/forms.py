from django import forms
from firstApp.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['videoLink']

    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance