from os import path
from pydub import AudioSegment

# imports
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import wave
import sys
import struct 
import time


CHUNK = 1024*2
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

# create matplotlib figure and axes
fig, ax = plt.subplots(1, figsize=(15, 7))

#Code for playing
# Instantiate PyAudio
p = pyaudio.PyAudio()
file_sw = obj.getsampwidth()

stream = p.open(format=p.get_format_from_width(file_sw),
                channels=obj.getnchannels(),
                rate=obj.getframerate(),
                output=True,
                frames_per_buffer=CHUNK)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)

# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# show the plot
plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

while True:
    
    # binary data
    
    data = obj.readframes(CHUNK) 
  
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2*CHUNK) + 'B', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    line.set_ydata(data_np)
    
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except :
        
        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break