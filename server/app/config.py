import os

SECRET_KEY = os.getenv('SECRET_KEY', default='!secret')
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
SQLALCHEMY_DATABASE_URI = "sqlite:///mydatabase.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
GOOGLE_CLIENT_ID = os.getenv('88355639443.apps.googleusercontent.com') #Update to yours
GOOGLE_CLIENT_SECRET = os.getenv('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') #update to yours