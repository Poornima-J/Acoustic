from os import path
from pydub import AudioSegment
import pyaudio
import wave
import sys

BUFFER_SIZE = 1024
print("Enter the audio file in mp3 format:- ")
src = input()
# files                                                                         
# src = "transcript.mp3"
dst = "test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

# Opening audio file as binary data
obj = wave.open(dst, 'rb')

# Instantiate PyAudio
p = pyaudio.PyAudio()
file_sw = obj.getsampwidth()

stream = p.open(format=p.get_format_from_width(file_sw),
                channels=obj.getnchannels(),
                rate=obj.getframerate(),
                output=True)

data = obj.readframes(BUFFER_SIZE)

while len(data)>0:
    stream.write(data)
    data = obj.readframes(BUFFER_SIZE)

stream.stop_stream()
stream.close()

p.terminate()
obj.close()

