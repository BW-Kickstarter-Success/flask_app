"""Database file.
SQLAlchemy models and utility functions for Twittoff
"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Project(DB.Model):
    """Kickstarter projects table
    """
    id = DB.Column(DB.String, primary_key=True)  # primary_key=True
    name = DB.Column(DB.String, nullable=False)
    category_name = DB.Column(DB.String)  # 'name'
    category_slug = DB.Column(DB.String)  # 'slug'
    goal_amount = DB.Column(DB.Float)  # 'money ($)'
    description = DB.Column(DB.String)  # 'blurb'
    launched_at = DB.Column(DB.DateTime)  # 'launched_at'
    deadline_at = DB.Column(DB.DateTime)  # 'deadline_at'
    country_code = DB.Column(DB.String)
    town = DB.Column(DB.String)

    def __repr__(self):
        return "<Project: {} >".format(self.name)
#  {'blurb', 'launched_at', 'deadline', 'money ($)', 'slug', 'name', 'country', 'town'

