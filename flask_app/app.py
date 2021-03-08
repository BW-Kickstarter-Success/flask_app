import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, Project
from .kickstarter import add_new_project
from .predict import make_prediction


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
        return render_template("base.html", projects=Project.query.all())

    @app.route('/request', methods=["POST"])
    @app.route('/request/<url>', methods=["GET"])
    def get_data():
        url = request.values["url"]
        try:
            if request.method == "POST":
                add_new_project(url)
                message = "Project successfully added to the DataBase!"
                info = ''

            info = Project.query.all()

        except Exception as e:
            info = ""
            message = "Error adding {}: {}".format(url, e)

        return render_template("request_data.html", info=info, message=message)

    @app.route('/predict', methods=['POST'])
    def predict():
        project = request.values['project']
        message = make_prediction(project)
        return render_template('request_data.html', title="Prediction", message=project)

    # reset/start the database
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        message = 'Database reset!'
        info = ''
        return render_template("request_data.html", info=info, message=message)

    return app
