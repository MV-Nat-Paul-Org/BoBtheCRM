from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from datetime import timedelta  # Import timedelta for session lifetime
from . import main  # Import your main route file

app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)

# Initialize OAuth extension for authentication
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Register your main route file
app.register_blueprint(main)

if __name__ == '__main__':
    app.run()

