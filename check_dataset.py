import audioplayer
import os
import tkinter
import threading

METADATA_LOCATION = "DBSpeech-1.0/metadata.csv" 
WAV_LOCATION = "DBSpeech-1.0/wavs/"
LINES_TO_SKIP = 1060

def parse_line(line):
    arr = line.split("|")
    return arr[0], arr[2]

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
    
def close_script():
    gui.quit()
    gui.destroy()
    os._exit(1)

def play_audio_loop():
    global LINES_TO_SKIP
    while True:
        line = metadata_file.readline()
        if not line:
            break
        wav_name, transcription = parse_line(line)
        canvas.delete('all')
        canvas.create_text(155,85,fill="darkblue",font="Times 12",
                            text=insert_newlines(transcription))
        if LINES_TO_SKIP == 0:
            ap = audioplayer.AudioPlayer(WAV_LOCATION + wav_name + ".wav")
            ap.play(block=True)
        else:
            LINES_TO_SKIP -= 1
    metadata_file.close()
    

if __name__ == '__main__':
    metadata_file = open(METADATA_LOCATION, 'r')
    
    gui = tkinter.Tk()
    gui.geometry("450x250")
    gui.title("TTS Dataset Maker")
    gui.protocol("WM_DELETE_WINDOW", close_script)
    canvas = tkinter.Canvas(gui, width=300, height=170, bg = '#afeeee')
    canvas.pack()
    play_audo_thread = threading.Thread(target=play_audio_loop)
    play_audo_thread.start()
    tkinter.mainloop()

