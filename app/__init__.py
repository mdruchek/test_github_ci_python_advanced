from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "key"
    from .database import db

    db.init_app(app)

    from .models import Client, ClientParking, Parking

    with app.app_context():
        db.drop_all()
        db.create_all()

    from . import routes

    app.register_blueprint(routes.bp)

    return app
