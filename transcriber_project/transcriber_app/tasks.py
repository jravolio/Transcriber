import whisper
from whisper.utils import get_writer as getwriter
from celery import shared_task
import subprocess
from .models import Videos
from pathlib import Path

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

@shared_task()
def transcribe_text_task(file_path):
    file_name = Path(file_path).stem
    audio_file = Path('./media/transcribes/audio_converted') / f'{file_name}.mp3'

    convert_video_to_audio_task(input_file=file_path, output_file=audio_file)

    model = whisper.load_model("small")
    result = model.transcribe(str(audio_file),initial_prompt="Esse é um vídeo falando sobre poker. André marques e Simon Brandstrom, opta por jogar de 3-bet para 20,000. não vai desistir desse Dama-Dez não, hein, Del. Flop Vala-Dez-Cinco, e agora?", word_timestamps=True)

    word_options = {
            "highlight_words": False,
            "max_line_count": 2,
            "max_line_width": 42
        }

    srt_writer = getwriter("srt", "./media/transcribes/srt_converted")
    srt_writer(result, str(audio_file), word_options)

    try:
        video_instance = Videos.objects.get(raw_file=f"transcribes/media/{file_name}.mp4")
        video_instance.srt_file = f'transcribes/srt_converted/{file_name}.srt'
        video_instance.save()
    except Videos.DoesNotExist:
        pass