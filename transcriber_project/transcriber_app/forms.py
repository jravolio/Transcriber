from django import forms
from .models import Videos

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = {'raw_file', 'title'}