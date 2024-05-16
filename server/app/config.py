# main configuration of app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

GOOGLE_CLIENT_ID = os.getenv('88355639443-db3h4ragup2r7e5c0jtb113ipubg317t.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.getenv('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')

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config['SQLALCHEMU_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)