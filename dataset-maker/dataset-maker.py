import audioplayer
import os
import tkinter
import threading
import pyaudio
import wave

import sentences

SENTENCE_ID = 0
IS_RECORDING = False
IS_PLAYING_BACK = True
IS_WRITING_SOUND_FILE = False
DONE_SENTENCES = []
SOUNDS_PATH = "sounds/"
SOUND_ID = -1
WAV_PREFIX = "speaker_"
METADATA_PATH = "metadata.csv"
METADATA_FILE = None

def load_metadata():
    global SOUND_ID
    global SENTENCE_ID
    global METADATA_FILE
    with open(METADATA_PATH, 'r') as file:
        line = file.readline()
        while line:
            SOUND_ID = int(line.split("|")[0][-3:])
            transcription = line.split("|")[2][:-1]
            DONE_SENTENCES.append(transcription)
            line = file.readline()
    SOUND_ID += 1
    
    try:
        while sentences.SENTENCES[SENTENCE_ID] in DONE_SENTENCES:
            SENTENCE_ID += 1
    except:
        print("All sentences are already in metadata file!")
        os._exit(1)
    
    METADATA_FILE = open(METADATA_PATH, 'a')

def insert_newlines(str):
    MAX_CHARS_IN_LINE = 45
    words = str.split()
    ret_str = ""
    chars_in_line = 0
    for word in words:
        chars_in_line += len(word) + 1
        if chars_in_line <= MAX_CHARS_IN_LINE:
            ret_str += word + " "
        else:
            ret_str += "\n" + word + " "
            chars_in_line = len(word) + 1
    return ret_str

def next_sentence():
    global SOUND_ID
    global SENTENCE_ID
    global IS_RECORDING
    global IS_WRITING_SOUND_FILE
    
    if IS_RECORDING:
        start_recording()
        IS_WRITING_SOUND_FILE = True
    
    while IS_WRITING_SOUND_FILE:
        continue
    
    # save metadata
    METADATA_FILE.write(WAV_PREFIX + "{:04d}".format(SOUND_ID) + "|" + sentences.SENTENCES[SENTENCE_ID] + "|" + sentences.SENTENCES[SENTENCE_ID] + "\n")
    SOUND_ID += 1
    
    SENTENCE_ID += 1
    if not sentences.SENTENCES[SENTENCE_ID]:
        close_script()
    canvas.delete('all')
    canvas.create_text(155,85,fill="darkblue",font="Times 12",
                        text=insert_newlines(sentences.SENTENCES[SENTENCE_ID]))
    
    
def start_recording():
    global IS_RECORDING
    IS_RECORDING = not IS_RECORDING
    if (IS_RECORDING):
        record_button['text'] = ("Stop recording")
    else:
        record_button['text'] = ("Start recording")
        
def play_recording():
    ap = audioplayer.AudioPlayer("output.wav")
    ap.play(block=True)
    
def close_script():
    METADATA_FILE.close()
    gui.quit()
    gui.destroy()
    os._exit(1)

def recording_loop():
    global IS_RECORDING
    global IS_WRITING_SOUND_FILE
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 22050
    #RECORD_SECONDS = 5
    #WAVE_OUTPUT_FILENAME = "output.wav"
    
    p = pyaudio.PyAudio()  
            
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)

    while (True):
        if (IS_RECORDING):
            print("* recording")

            frames = []

            while (IS_RECORDING):
                data = stream.read(CHUNK)
                frames.append(data)

            print("* done recording")

            #stream.stop_stream()
            #stream.close()
            #p.terminate()

            wf = wave.open(SOUNDS_PATH + WAV_PREFIX + "{:04d}".format(SOUND_ID) + ".wav", 'wb')
            IS_WRITING_SOUND_FILE = False
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

if __name__ == '__main__':
    load_metadata()
    gui = tkinter.Tk()
    gui.geometry("450x250")
    gui.title("TTS Dataset Maker")
    gui.protocol("WM_DELETE_WINDOW", close_script)
    #volume_slider = tkinter.Scale(gui, from_=0, to=100, orient=tkinter.HORIZONTAL, command=update_volume)
    #volume_slider.set(100)
    #volume_slider.pack()
    canvas = tkinter.Canvas(gui, width=300, height=170, bg = '#afeeee')
    canvas.create_text(155,85,fill="darkblue",font="Times 12",
                        text=insert_newlines(sentences.SENTENCES[SENTENCE_ID]))
    canvas.pack()
    #sentence_text = tkinter.Text(gui, state='disabled', width=44, height=5)
    #sentence_text.tag_configure("center", justify='center')
    #sentence_text.configure(state='normal')
    #sentence_text.insert('1.0', 'This is a Text widget demo This is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demoThis is a Text widget demo')
    #sentence_text.tag_add("center", "1.0", "end")
    #sentence_text.configure(state='disabled')
    #sentence_text.pack()
    record_button = tkinter.Button(gui, text='Start recording', command=start_recording)
    record_button.pack()
    recording_thread = threading.Thread(target=recording_loop)
    recording_thread.start()
    #tkinter.Button(gui, text='Play recording', command=play_recording).pack()
    tkinter.Button(gui, text='Next sentence', command=next_sentence).pack()
    tkinter.mainloop()

