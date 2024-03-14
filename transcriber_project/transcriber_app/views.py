from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from openai import OpenAI
from .forms import FileUploadForm
from .models import Videos
import subprocess
import os
from .tasks import transcribe_text_task
from dotenv import load_dotenv
from pathlib import Path


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


def download_file(request, file):
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
    load_dotenv()
    file_name = file.raw_file.path.split('/')
    file_name = file_name[-1].split('.')
    print('esse é o file_name')
    file_path = file.raw_file.path
    file_name = Path(file.raw_file.path).stem
    audio_file_path = Path(__file__).resolve().parent.parent / 'media' / 'transcribes' / 'audio_converted' / f'{file_name}.mp3'
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    convert_video_to_audio_task(input_file=file_path, output_file=audio_file_path)

    audio_file = open(f"{audio_file_path}", "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="srt",
        timestamp_granularities=["segment"]
    )
    
    with open(Path(__file__).resolve().parent.parent / 'media' / 'transcribes' / 'srt_converted' / f'{file_name}.srt', 'a', encoding='utf-8') as file:
        file.write(transcript)
    
    print(transcript)

    try:
        video_instance = Videos.objects.get(raw_file=f"transcribes/media/{file_name}.mp4")
        video_instance.srt_file = f'transcribes/srt_converted/{file_name}.srt'
        video_instance.save()
    except Videos.DoesNotExist:
        pass


def convert_video_to_audio_task(input_file, output_file, audio_bitrate='32k'):
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-i', input_file,
        '-vn',
        '-b:a', audio_bitrate,
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Audio conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
