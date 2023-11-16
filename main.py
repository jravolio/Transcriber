from whisper.utils import get_writer as getwriter
import subprocess
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

input_file = 'video.mp4'
output_file = './teste/audio.mp3'
audio_bitrate = '32k'
prompt = "Esse é um vídeo falando sobre poker. Badziakouski e Watson, opta por jogar de 3-bet para 20,000. não vai desistir desse Dama-Dez não, hein, Del. Flop Vala-Dez-Cinco, e agora?"
convert_video_to_audio(input_file, output_file, audio_bitrate)


# audio_file= open("audio.mp3", "rb")
# model = whisper.load_model("small")
# result = model.transcribe("audio.mp3",initial_prompt="prompt", word_timestamps=True)
# print(result["text"])

# model = whisper.load_model("base")

# # load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("audio.mp3")
# audio = whisper.pad_or_trim(audio)

# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")

# # decode the audio
# options = whisper.DecodingOptions(fp16 = False)
# result = whisper.decode(model, mel, options)

# # print the recognized text
# print(result.text)

audio_file= open("audio.mp3", "rb")
model = whisper.load_model("large")
result = model.transcribe("audio.mp3",initial_prompt=prompt, word_timestamps=True)
print(result["text"])
word_options = {
        "highlight_words": False,
        "max_line_count": 2,
        "max_line_width": 16
    }
srt_writer = getwriter("srt", "./")
srt_writer(result, 'audio.mp3', word_options)