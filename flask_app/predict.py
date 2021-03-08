from tensorflow import keras
from .models import Project


def make_prediction(project):
    project = Project.query.filter(Project.name == project).one()
    saved_model = keras.models.load_model('../my_model/saved_model.pb')
    # prediction = saved_model.predict(project)
    return saved_model, project
