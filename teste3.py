import json
from datetime import datetime

with open('response2.json', 'r', encoding='utf-8') as f:
    fjdata = json.load(f)
    count = 1
    words_buffer = []
    for word in fjdata:
        words_buffer.append(word)
        with open('teste.srt', 'a', encoding='utf-8') as file:
            if len(words_buffer) >= 10:
                file.write(str(count) + '\n')
                start_time = datetime.utcfromtimestamp(word['start']).strftime('%H:%M:%S,%f')[:-3]
                end_time = datetime.utcfromtimestamp(word['end']).strftime('%H:%M:%S,%f')[:-3]
                file.write(start_time + ' --> ' + end_time + '\n')

                for item in words_buffer:
                    file.write(str(item["word"] + ' '))

                file.write('\n\n')
                words_buffer = []
                count+=1
    print(words_buffer)