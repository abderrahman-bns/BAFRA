import os
import secrets

from PIL import Image
from flask import render_template, url_for, redirect, request, flash, Response
from flask_login import logout_user, current_user, login_required, login_user
from flask_mail import Message
from werkzeug.utils import secure_filename

from faceApp import ALLOWED_EXTENSIONS
from faceApp import app, bcrypt, mail, db
from faceApp.bounding_box import CameraTest
from faceApp.create_db import create_db
from faceApp.encode_face import create_encoding
from faceApp.face_recognition import Camera
from faceApp.forms import LoginForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm, ResetForm, ContactForm
from faceApp.models import User


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='home')


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'All fields are required.', 'danger')
            return render_template('contact.html', title='contact', form=form)
        else:
            msg = Message(form.subject.data, sender=form.email.data, recipients=['abderrahmanbns21@gmail.com'])
            msg.body = """
                  From: %s &lt;%s&gt;
                  %s
                  """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', title='contact', success=True)
    elif request.method == 'GET':
        return render_template('contact.html', title='contact', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Login Unsuccessful. Please check email and password", "danger")
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/saveVideo', methods=['GET', 'POST'])
@login_required
def saveVideo():
    if request.method == 'POST':
        # check if the post request has the file part
        if not os.path.exists(
                'G:/PROJET/PYTHON/FACE_RECOGNITION/Real_time_face_recognition_with_GPU_FLASK_V2/faceApp/static/dataset/vid/' + current_user.agent.nom + '_' + current_user.agent.prenom):
            os.makedirs(
                'G:/PROJET/PYTHON/FACE_RECOGNITION/Real_time_face_recognition_with_GPU_FLASK_V2/faceApp/static/dataset/vid/' + current_user.agent.nom + '_' + current_user.agent.prenom)
            print("Directory ",
                  'G:/PROJET/PYTHON/FACE_RECOGNITION/Real_time_face_recognition_with_GPU_FLASK_V2/faceApp/static/dataset/vid/' + current_user.agent.nom + '_' + current_user.agent.prenom,
                  " Created ")
        else:
            print("Directory ",
                  'G:/PROJET/PYTHON/FACE_RECOGNITION/Real_time_face_recognition_with_GPU_FLASK_V2/faceApp/static/dataset/vid/' + current_user.agent.nom + '_' + current_user.agent.prenom,
                  " already exists")

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'] + '/' + current_user.agent.nom + '_' + current_user.agent.prenom,
                current_user.agent.nom + '_' + current_user.agent.prenom + '.mp4'))
            current_user.video_file = current_user.agent.nom + '_' + current_user.agent.prenom + '.mp4'
            db.session.commit()
            flash(f'Your video has been uploaded!', 'success')
            return redirect(url_for('account', filename=filename))
    return render_template('save_video.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(CameraTest()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/face_recognition')
def face_recognition():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/face-id')
def faceID():
    return render_template('face_recognition.html')


@app.route('/bounding-box')
def boundingBox():
    return render_template('bounding_box.html')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='bafra@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/reset", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetForm()
    user = User.query.filter_by(email=current_user.email).first()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash(f'Your password has been updated!', 'success')
            return redirect(url_for('reset_password'))
        elif user.password != form.old_password.data:
            flash(f"Update Unsuccessful. Please check your password", "danger")
        else:
            flash(f"Update Unsuccessful.", "danger")
    return render_template('reset.html', title='Reset Password', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.agent.age = form.age.data
        current_user.agent.tel = form.tel.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.nom.data = current_user.agent.nom
        form.prenom.data = current_user.agent.prenom
        form.email.data = current_user.email
        form.profile.data = current_user.profile
        form.age.data = current_user.agent.age
        form.tel.data = current_user.agent.tel
        form.sex.data = current_user.agent.sex
        form.video_file.data = current_user.video_file
        form.fonction.data = current_user.agent.fonction
        form.departement.data = current_user.agent.departement.nom
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/account-cdb")
@login_required
def createdDB():
    try:
        create_db()
        flash(f'The database has been successfully created!', 'success')
        return redirect(url_for('account'))
    except:
        flash(f'The creation of the database failed!!', 'danger')


@app.route("/account-cen")
@login_required
def createEN():
    try:
        create_encoding()
        flash(f'The encoding file has been successfully created!', 'success')
        return redirect(url_for('account'))
    except:
        flash(f'The creation of the encoding file failed!!', 'danger')


@app.route("/manage_account", methods=['GET', 'POST'])
@login_required
def manage_agent():
    users = User.query.all()
    return render_template('manage_agent.html', users=users, title='Manage Account')


@app.route("/manage_account/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_agent(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.agent.age = form.age.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('manage_agent', user_id=user.id))
    elif request.method == 'GET':
        form.user_id.data = user.id
        form.username.data = user.username
        form.nom.data = user.agent.nom
        form.prenom.data = user.agent.prenom
        form.email.data = user.email
        form.profil.data = user.profil
        form.age.data = user.agent.age
        form.sex.data = user.agent.sex
        form.fonction.data = user.agent.fonction
        form.departement.data = user.agent.departement.nom
    return render_template('update_agent.html', title='Update Account', form=form)


@app.route("/record", methods=['GET'])
@login_required
def record():
    return render_template('record.html')
