from os import path
from pydub import AudioSegment

# imports
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import wave
import sys

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

# #Code for playing
# # Instantiate PyAudio
# p = pyaudio.PyAudio()
# file_sw = obj.getsampwidth()

# stream = p.open(format=p.get_format_from_width(file_sw),
#                 channels=obj.getnchannels(),
#                 rate=obj.getframerate(),
#                 output=True)

# data = obj.readframes(-1)

# while len(data)>0:
#     stream.write(data)
#     data = obj.readframes(-1)

signal = obj.readframes(-1)
signal = np.frombuffer(signal, dtype ="int16")
      
    # gets the frame rate
f_rate = obj.getframerate()
  
    # to Plot the x-axis in seconds 
    # you need get the frame rate 
    # and divide by size of your signal
    # to create a Time Vector 
    # spaced linearly with the size 
    # of the audio file
time = np.linspace(
    0, # start
    len(signal) / f_rate,
    num = len(signal)
)
  
    # using matlplotlib to plot
    # creates a new figure
plt.figure(1)
plt.axis("off")
      
    # title of the plot
# plt.title("Sound Wave")
      
    # label of x-axis
# plt.xlabel("Time")
     
    # actual ploting
plt.plot(time, signal)
      
    # shows the plot 
    # in new window
plt.show()

# stream.stop_stream()
# stream.close()

# p.terminate()
obj.close()

