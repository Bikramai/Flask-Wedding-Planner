from flask import Flask, redirect, url_for

from .auth import auth
from .customer import customer
from .todo import todo
from .extns import db, login_manager, bcrypt
from .model import Account
from .vendor import vendor
from .chat import chat


class Config:
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    UPLOADS_FOLDER = './weddingPlanner/static/uploads'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth)
    app.register_blueprint(vendor)
    app.register_blueprint(customer)
    app.register_blueprint(todo)
    app.register_blueprint(chat)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        import weddingPlanner.model
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return Account.query.get(int(user_id))

    @app.route("/")
    def index():
        return redirect(url_for("customer.index"))

    return app
