import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB
from .kickstarter import request_data


load_dotenv()


def create_app():
    """
    Creating and configuring an instance
    of the Flask application

    :return: an instance of the Flask app
    """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template("base.html")

    @app.route('/request')
    def get_data():
        url = request.values["url"]
        info = request_data("{}".format(url))
        return render_template("request_data.html", info=info)

    # reset/start the database
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return "Database reset!"

    return app
