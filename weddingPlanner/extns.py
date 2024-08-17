import os.path
import uuid

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import current_app

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def save_form_images(images, vendor):
    if not os.path.exists(f"{current_app.config['UPLOADS_FOLDER']}/{vendor}"):
        os.makedirs(f"{current_app.config['UPLOADS_FOLDER']}/{vendor}")

    filenames = []

    for image in images:
        filename = str(uuid.uuid4()) + "." + image.filename.split(".")[-1]
        image.save(os.path.join(f"{current_app.config['UPLOADS_FOLDER']}", filename))
        filenames.append(filename)

    return filenames
