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


app.config['UPLOAD_EXTENSIONS'] = ['.mp3']
app.config['UPLOAD_PATH'] = 'uploads'


@app.route('/index')
@login_required
def index():
    return render_template('index.html',title='Home Page')


@app.route('/')
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
    return render_template('user.html',user=user)


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
            os.system('python3 app/core.py '+str(src.filename)) 
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
