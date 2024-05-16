from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Initialize OAuth extension for authentication
google_blueprint = make_google_blueprint(
    client_id="YOUR_GOOGLE_CLIENT_ID", # Replace with your Google client ID
    client_secret="YOUR_GOOGLE_CLIENT_SECRET", # Replace with your Google client secret
    scope=["profile", "email"],
    redirect_url="/google-login"
)
app.register_blueprint(google_blueprint, url_prefix="/login")

