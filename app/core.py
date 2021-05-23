# imports
import matplotlib.pyplot as plt
import numpy as np
import librosa.display 
import pygame 
import os
import wave
import subprocess
import mutagen
import sys
import moviepy.editor as mpe
import time
from mutagen.wave import WAVE
from os import path
from pydub import AudioSegment

def convert_seq_to_mov():
    input = r"image%04d.jpg"
    output = r"downloads/"+str(src)[:-4]+".mp4"
    cmd = f'ffmpeg -framerate {frame_rate} -i "{input}" "{output}"'
    print(cmd)
    subprocess.check_output(cmd, shell=True)

def make_video(screen):
    image_num = 0
    while True:
        image_num += 1
        str_num = "000" + str(image_num)
        file_name = "image" + str_num[-4:] + ".jpg"
        pygame.image.save(screen, file_name)
        yield

def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioBar:
    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.freq = x, y, freq
        self.color = "#FF00FF"
        self.width, self.min_height, self.max_height = width, min_height, max_height
        self.height = min_height
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)
    def update(self, dt, decibel):
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height += speed * dt
        self.height = clamp(self.min_height, self.max_height, self.height)
    def render(self, screen):
            pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))

src=sys.argv[1]

# files                                                                         
dst = "test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3("uploads/"+src)
sound.export(dst, format="wav")

# function to convert the information into some readable format
def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
  
    return hours, mins, seconds  # returns the duration
  
# Create a WAVE object Specify the directory address of your wavpack file
audio = WAVE(dst)
  
# contains all the metadata about the wavpack file
audio_info = audio.info
length = audio_info.length

#getting information about file
time_series, sample_rate = librosa.load(dst)

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

# converting the matrix to decibel matrix
spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

# getting an array of frequencies
frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
time_index_ratio = len(times)/times[len(times) - 1]
frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

def get_decibel(self, target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio )][int(target_time * time_index_ratio)]

pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w/2.5)
screen_h = int(infoObject.current_w/2.5)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])

pygame.display.set_caption(src)

background = pygame.image.load("image/image2.jpg")

bars = []


frequencies = np.arange(100, 8000, 100)

r = len(frequencies)


width = screen_w/r


x = (screen_w - (width*r))/2

for c in frequencies:
    bars.append(AudioBar(x, 300, c, (255, 0, 0), max_height=400, width=width))
    x += width

t = pygame.time.get_ticks()
getTicksLastFrame = t
count=0
pygame.mixer.music.load(dst)
pygame.mixer.music.play(0)

save_screen = make_video(screen)  # initiate the video generator
video = True  # at start: video not active
count=0

# Run until the user asks to quit
running = True
begin=end=time.time()
while running:

    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    
    if (end-begin)>=length :
        running=False
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            video = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    #background image
    screen.blit(background,(0,0))

    for b in bars:
        b.update(deltaTime, get_decibel(b,pygame.mixer.music.get_pos()/1000.0, b.freq))
        b.render(screen)
        
    # Flip the display
    pygame.display.flip()

    end=time.time()
    if video:
        next(save_screen) 
        count+=1 # call the generator

# Done! Time to quit pygame screen.
pygame.quit()

# To determine fps for converting audio to video
frame_rate=count/length
convert_seq_to_mov()

#Combine auido and video
clip = mpe.VideoFileClip("downloads/"+str(src)[:-4]+".mp4")
audio_bg = mpe.AudioFileClip("uploads/"+str(src))
final_clip = clip.set_audio(audio_bg)
final_clip.write_videofile("downloads/"+str(src)[:-4]+"2.mp4")

#code to delete audio,video and image files
os.remove("uploads/"+src) 
os.remove("test.wav")
os.remove("downloads/"+str(src)[:-4]+".mp4")
test = os.listdir(".")
for images in test:
    if images.endswith(".jpg"):
        os.remove(os.path.join(".", images))