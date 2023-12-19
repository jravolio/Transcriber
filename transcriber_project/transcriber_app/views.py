from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from .forms import FileUploadForm
from .models import Videos
import subprocess
import os
from .tasks import transcribe_text_task

def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            transcribe_text(form.save())
            return redirect('/')
    else:
        form = FileUploadForm()
        
    return render(request, "transcriber/upload.html", {
        'form': form
    })

def download_file(request,file):
    file_path = os.path.realpath(file)
    response = FileResponse(open(file_path, 'rb'))
    file_name = os.path.basename(file_path)
    video_instance = Videos.objects.get(srt_file=f'transcribes/srt_converted/{file_name}')
    response['Content-Disposition'] = f'inline; filename={video_instance.title}.srt'
    return response

def transcribed_list(request):
    videos = Videos.objects.all()
    return render(request, "transcriber/transcribed_list.html", {
        'videos': videos
    })

def transcribe_text(file):
    file_name = file.raw_file.path.split('/')
    file_name = file_name[-1].split('.')
    print(file_name[0])
    
    transcribe_text_task.delay(file.raw_file.path)