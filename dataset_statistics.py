import os
import wave
import contextlib
import re
import string

WAVS_PATH = "DBSpeech-1.0/wavs/"
METADATA_PATH = "DBSpeech-1.0/metadata.csv"

directory = os.fsencode(WAVS_PATH)

total_duration = 0
total_words = 0
total_chars = 0
durations = []
words_per_clip = []
transcriptions = []
unique_words = set()

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    with contextlib.closing(wave.open(WAVS_PATH + filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        durations.append(duration)
        total_duration += duration
        
with open(METADATA_PATH, 'r') as file:
    line = file.readline()
    while line:
        transcription = line.split("|")[2]
        total_chars += len(transcription)
        for word in transcription.split():
            pattern = re.compile('[\W_]+')
            total_words += 1
            # remove non-alphanumeric chars
            pattern.sub(word, string.printable)
            word = word.lower()
            if word:
                unique_words.add(word)
        transcriptions.append(transcription)
        line = file.readline()
        
 
print("Total Clips            %s" % f'{len(durations):,}') 
print("Total Words            %s" % f'{total_words:,}') 
print("Total Characters       %s" % f'{total_chars:,}') 
print("Total Duration         %02d:%02d:%02d" % (int(total_duration / 3600), int(total_duration % 3600 / 60), int(total_duration % 60))) 
print("Mean Clip Duration     %.2f sec" % (total_duration / len(durations))) 
print("Min Clip Duration      %.2f sec" % min(durations)) 
print("Max Clip Duration      %.2f sec" % max(durations)) 
print("Mean Words per Clip    %.2f" % (total_words / len(durations))) 
print("Distinct Words         %s" % f'{len(unique_words):,}') 
        
#Total Clips            1,065
#Total Words            13,144
#Total Characters       75,887
#Total Duration         1:19:49
#Mean Clip Duration     4.50 sec
#Min Clip Duration      0.31 sec
#Max Clip Duration      15.60 sec
#Mean Words per Clip    12.34
#Distinct Words         3,094
