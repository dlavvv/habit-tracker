import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'idk-man-u-tell-me'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///habit-tracker.sqlite3'

    SQLALCHEMY_TRACK_MODIFICATIONS = False