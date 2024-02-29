import json
from datetime import datetime

def create_srt_from_json(json_file, output_file, buffer_size=10):
    with open(json_file, 'r', encoding='utf-8') as f:
        fjdata = json.load(f)
        count = 1
        words_buffer = []
        with open(output_file, 'a', encoding='utf-8') as file:
            for word in fjdata:
                words_buffer.append(word)
                if len(words_buffer) >= buffer_size:
                    file.write(str(count) + '\n')
                    start_time = datetime.utcfromtimestamp(words_buffer[0]['start']).strftime('%H:%M:%S,%f')[:-3]
                    end_time = datetime.utcfromtimestamp(words_buffer[-1]['end']).strftime('%H:%M:%S,%f')[:-3]
                    file.write(start_time + ' --> ' + end_time + '\n')

                    for item in words_buffer:
                        file.write(str(item["word"] + ' '))

                    file.write('\n\n')
                    words_buffer = []
                    count += 1

if __name__ == "__main__":
    create_srt_from_json('response2.json', 'teste.srt')
    print("Arquivo .srt criado com sucesso!")
