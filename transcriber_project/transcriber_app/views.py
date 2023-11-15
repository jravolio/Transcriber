from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from .forms import FileUploadForm
from .models import Videos

def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = FileUploadForm()
        
    return render(request, "transcriber/upload.html", {
        'form': form
    })

def transcribed_list(request):
    videos = Videos.objects.all()
    return render(request, "transcriber/transcribed_list.html", {
        'videos': videos
    })