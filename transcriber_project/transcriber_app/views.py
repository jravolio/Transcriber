from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from whisper.utils import get_writer as getwriter
from .forms import FileUploadForm
from .models import Videos
import subprocess
import whisper
import os

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

def convert_video_to_audio(input_file, output_file, audio_bitrate='32k'):
    print('converting video to audio')
    # Construct the FFmpeg command as a list of arguments
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-i', input_file,
        '-vn',         # Disable video processing
        '-b:a', audio_bitrate,
        output_file
    ]

    try:
        # Execute the FFmpeg command
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Audio conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def transcribe_text(file):
    print('transcribing text')
    print('esse é o raw_file path' + file.raw_file.path)
    file_name = file.raw_file.path.split('/')
    file_name = file_name[-1].split('.')
    print(file_name[0])
    convert_video_to_audio(input_file=file.raw_file.path, output_file=f'./media/transcribes/audio_converted/{file_name[0]}.mp3')

    model = whisper.load_model("small")
    result = model.transcribe(f"media/transcribes/audio_converted/{file_name[0]}.mp3",initial_prompt="Esse é um vídeo falando sobre poker. Badziakouski e Watson, opta por jogar de 3-bet para 20,000. não vai desistir desse Dama-Dez não, hein, Del. Flop Vala-Dez-Cinco, e agora?", word_timestamps=True)
    print(result["text"])
    word_options = {
            "highlight_words": False,
            "max_line_count": 2,
            "max_line_width": 16
        }
    srt_writer = getwriter("srt", "./media/transcribes/srt_converted")
    srt_writer(result, f'media/transcribes/audio_converted/{file_name[0]}.mp3', word_options)

    video_instance = Videos.objects.get(raw_file=file.raw_file)
    video_instance.srt_file = f'transcribes/srt_converted/{file_name[0]}.srt'
    video_instance.save()
