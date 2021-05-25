![BFH Banner](https://trello-attachments.s3.amazonaws.com/542e9c6316504d5797afbfb9/542e9c6316504d5797afbfc1/39dee8d993841943b5723510ce663233/Frame_19.png)

# Acoustic

> Visualize what you want to hear  

## Table of Contents

- [Description](#Description)
- [Team Members](#Team-Members)
- [Team Id](#Team-Id)
- [Link to product walkthrough](#Link-to-product-walkthrough)
- [How it Works ?](#How-it-Works)
- [Libraries used](#Libraries-used)
- [How to configure ?](#How-to-configure)
- [How to Run ?](#How-to-Run)

## Description
Who doesn't love listening to some music ? Have you ever thought how nice it would be, if we can visulaise the music we love to hear ?. It would be a visual treat for our eyes and a blessing for our ears.
If you feel so, then test our project and make learning a fun experience.

This project is a audio visualising web application in which a potential user can create a user account by entering a valid username, password, email id through the Register option 
or if the user already has an account then he/she can sign up with the credentials.After you login,in the home page you will be greated with a warm welcome note that briefly explains how to use the web app.
You can preview the details that you gave at the time of acoount creation in the My Profile Page. 

The prime function of this web app,that is to create a visualization of audio is being implemented in convertor page. Here there is an option to upload an audio in mp3 format and with the convert option
and get it converted to a video file which has a really pretty background.The user also has an option to download the generated video too. 
The user also can log out of their account using logout option.If they had checked the remember me option,then the next time they open the website, they will be automatically signed in.

## Team members
1. [Alphi Kurian Shajan](https://github.com/Alphi-Shajan)
2. [Gayathri Sivakumar Menon](https://github.com/gayathrismenon)
3. [Poornima J](https://github.com/Poornima-J)

## Team Id
BFH/recxwXAZaQIWv0B3n/2021

## Link to product walkthrough
[click here](https://www.loom.com/share/b55388273f37433d872b0484607ce68f)

## How it Works
1. Once you run the project, the first thing that you will see on your web browser is a Sign in Page, which has 2 options.  
   - If you are a new user,that is you don't have an account in this web app then you can create a new one by clicking on Register option and filling out username, email and a password.  
   - If you already have an account then, just use your login credentials and if you select Remember me option then the next time you login, you can automatically sign in.  
2. Next comes the home page , where you are welcomed by a welcome note which details on what does this web app really do and on which page is this functionality executed.  
3. There a My profile page which lists the details that you gave while creating an account
4. Then comes Convertor page which has the browse option to upload an audio file in mp3 format and the convert option enables you to convert the audio that you just entered into a video which contains a pretty good visualisation of audio. 
5. While the convertion process is going on you can see the visualisation of the audio as an pop up screen 
6. After the conversion process is compleated you are redirected to download page where there is a download option through which you can download the final video
7. There is also a logout page through which you can logout of the web app.

## Libraries used
matplotlib==3.4.2, numpy==1.20.3, librosa==0.8.0, pygame==2.0.1, Wave==0.0.2,mutagen==1.45.1, moviepy==1.0.3, pydub==0.25.1,Flask==2.0.0, Flask-Login==0.5.0, Flask-Migrate==3.0.0, Flask-SQLAlchemy==2.5.1, Flask-WTF==0.14.3

## How to configure

**Setting up Flask**
1. First install python in your computer acoording to your system configurations if you don't have it and make sure it is functional by typing in `python` or `python3` in the terminal.  
2. Create a directory for your project and move to that directory, say microblog.  
3. create a virtual environment in this directory by typing in the command `python3 -m venv venv`(for windows) and 
`sudo apt-get install virtualenv` (for linux).  
4. To activate your brand new virtual environment you use the following command `source venv/bin/activate` OR `venv/Scripts/activate` (for windows) and `virtualenv venv` (for linux)
5. Now install flask in it using command: `pip install flask`
6. Create a package called app,inside the microblog, using the following command: `mkdir app`.  
7. Create an `__init__.py` for app.  
8. The routes are the different URLs that the application implements. In Flask, handlers for the application routes are written as Python functions, called view functions. View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.so create a `routes.py` in app
9. To complete the application, you need to have a Python script at the top-level that defines the Flask application instance. so create a `microblog.py`
10. now type in terminal `export FLASK_APP=microblog.py` or `set FLASK_APP=microblog.py`(for windows)  
11. now type in terminal `flask run`
12. Go to `http://localhost:5000/` to see ur application.  
13. In Flask, templates are written as separate files, stored in a templates folder that is inside the application package.So create a folder templates ,inside the app, using the following command: `mkdir templates`
14. The operation that converts a template into a complete HTML page is called rendering. To render the template we import a function that comes with the Flask framework called `render_template()`. This function takes a template filename and a variable list of template arguments and returns the same template, but with all the placeholders in it replaced with actual values.Templates also support control statements, given inside `{% ... %}` blocks
16. To handle the web forms in the application we use the Flask-WTF extension, which is a thin wrapper around the WTForms package that nicely integrates it with Flask. 
```
$ pip install flask-wtf
```
**Setting up Database**
```
$ pip install flask-sqlalchemy
```
This is an extension that provides a Flask-friendly wrapper to the popular SQLAlchemy package, which is an Object Relational Mapper or ORM.

```
$ pip install flask-migrate
```
This extension is a Flask wrapper for Alembic, a database migration framework for SQLAlchemy.In `__init__.py `, add a `db` object that represents the database. Then add another object that represents the migration engine.`models`  module is impoted which will define the structure of the database.The `flask db migrate` command does not make any changes to the database, it just generates the migration script. To apply the changes to the database, the `flask db upgrade command` must be used.  
```
$ pip install flask-login
```
This extension manages the user logged-in state, so that for example users can log in to the application and then navigate to different pages while the application "remembers" that the user is logged in. It also provides the "remember me" functionality that allows users to remain logged in even after closing the browser window.  
```
$ pip install email-validator
```
The `Email()` validator from WTForms requires an external dependency to be installed.

**Installing necessary python modules**
```
pip install matplotlib
```
Matplotlib is a plotting library for the Python programming language and it's numerical mathematics extension NumPy library
```
pip install librosa
```
librosa is a python package for music and audio analysis. It provides the building blocks necessary to create music information retrieval systems.  
```
pip install pygame
```
Pygame is a cross-platform set of Python modules designed for writing video games.  
```
pip install os
```
The OS module in Python provides functions for interacting with the operating system.  
```
pip install wave
```
The wave module in Python's standard library is an easy interface to the audio WAV format.  
```
pip install subprocess
```
 It helps to obtain the input/output/error pipes as well as the exit codes of various commands.  
 ```
pip install mutagen
```
Mutagen is a Python module to handle audio metadata.  
```
pip install moviepy
```
MoviePy is a Python library for video editing: cutting, concatenations, title insertions, video compositing (a.k.a. non-linear editing), video processing, and creation of custom effects.

## How to Run
Instructions for running
