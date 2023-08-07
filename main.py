import subprocess
# import openai
import whisper.utils
import whisper

def convert_video_to_audio(input_file, output_file, audio_bitrate='32k'):
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


# openai.api_key = "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"
# input_file = 'video.mp4'
# output_file = 'audio.mp3'
# audio_bitrate = '32k'
# convert_video_to_audio(input_file, output_file, audio_bitrate)
# audio_file= open("audio.mp3", "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="srt", prompt="Esse é um vídeo falando sobre poker. Ele opta por jogar de 3-bet, não vai desistir desse Dama-Dez não, hein, Del. Flop Vala-Dez-Cinco, e agora?", word_timestamps=True, max_line_width=5, max_line_count=2)
# print(transcript)

input_file = 'video.mp4'
output_file = 'audio.mp3'
audio_bitrate = '32k'
convert_video_to_audio(input_file, output_file, audio_bitrate)
audio_file= open("audio.mp3", "rb")
model = whisper.load_model("small")
result = model.transcribe("audio.mp3", response_format="srt",initial_prompt="Esse é um vídeo falando sobre poker. Ele opta por jogar de 3-bet, não vai desistir desse Dama-Dez não, hein, Del. Flop Vala-Dez-Cinco, e agora?", word_timestamps=True)
print(result["text"])
# transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="srt", prompt="Esse é um vídeo falando sobre poker. Ele opta por jogar de 3-bet, não vai desistir desse Dama-Dez não, hein, Del. Flop Vala-Dez-Cinco, e agora?", word_timestamps=True, max_line_width=5, max_line_count=2)
# print(transcript)

# import whisper_timestamped as whisper
# from whisper.utils import get_writer

# input_file = 'video.mp4'
# output_file = 'audio.mp3'
# audio_bitrate = '32k'
# convert_video_to_audio(input_file, output_file, audio_bitrate)
# audio = whisper.load_audio("audio.mp3")
# model = whisper.load_model("tiny", device="cpu")
# result = whisper.transcribe(model, audio, beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0), initial_prompt="Esse é um vídeo falando sobre poker. Ele opta por jogar de 3-bet, não vai desistir desse Dama-Dez não, hein, Del. Flop Vala-Dez-Cinco, e agora?")
# import json
# print(json.dumps(result, indent = 2, ensure_ascii = False))
