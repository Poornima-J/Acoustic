import os
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User,FileContents
from flask import render_template,flash,redirect,url_for, request,abort, send_file
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask import send_from_directory
import threading
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

def main(filename):
    def convert_seq_to_mov():
        input = r"image%04d.jpg"
        output = r"app/downloads/"+str(src)[:-4]+".mp4"
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

    src=filename

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
    clip = mpe.VideoFileClip("app/downloads/"+str(src)[:-4]+".mp4")
    audio_bg = mpe.AudioFileClip("uploads/"+str(src))
    final_clip = clip.set_audio(audio_bg)
    final_clip.write_videofile("app/downloads/"+str(src)[:-4]+"2.mp4")

    #code to delete audio,video and image files
    os.remove("uploads/"+src)
    os.remove("test.wav")
    os.remove("app/downloads/"+str(src)[:-4]+".mp4")
    test = os.listdir(".")
    for images in test:
        if images.endswith(".jpg"):
            os.remove(os.path.join(".", images))


app.config['UPLOAD_EXTENSIONS'] = ['.mp3']
app.config['UPLOAD_PATH'] = 'uploads'
t = threading.Thread()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user={'username':'Miguel'}
    posts=[
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Kavya'},
            'body': 'My favourite cuisine is Chinese'
        }
    ]
    return render_template('index.html',title='Home Page',posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Sign In', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    posts=[
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',user=user,posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html',title='Audio to video visualizer')

@app.route('/success', methods = ['POST'])
@login_required
def success():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        src = request.files['file']
        filename = secure_filename(src.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if src.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            src.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            t = threading.Thread(target=main, args=(src.filename,))
            t.daemon = True
            t.start()
            #return redirect(url_for('uploaded_file',filename=filename))
            return redirect('/downloads/'+ str(src.filename)[:-4]+"2.mp4")
        return render_template("success.html", name = src.filename)


# Download API
@app.route("/downloads/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = "downloads/" + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')
