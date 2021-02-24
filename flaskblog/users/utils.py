from flask import Blueprint
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

util = Blueprint('util', __name__)




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Request Request', sender='nici.hahn@web.de', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    '''
    mail.send(msg)

def save_picture(form_picture):
    #create own file name with a length of 8 hex
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename) # _, -> filename is not used/needed
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(curent_app.root_path, 'static/profile_pics', picture_fn)
    #resize image to max 125 pixel to reduce storage on server 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size) 
    i.save(picture_path)
    return picture_fn