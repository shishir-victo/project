import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# configure the database with SQLite for local development
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///attendance.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# AWS config
app.config["AWS_ACCESS_KEY"] = os.environ.get("AWS_ACCESS_KEY", "")
app.config["AWS_SECRET_KEY"] = os.environ.get("AWS_SECRET_KEY", "")
app.config["S3_BUCKET"] = os.environ.get("S3_BUCKET", "student-attendance-images")
app.config["AWS_REGION"] = os.environ.get("AWS_REGION", "us-east-1")

# Configure max content length (20MB) for image uploads
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

# initialize the app with the extension
db.init_app(app)

# Configure login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Import and initialize login user loader
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    # Import models before creating tables
    import models  # noqa: F401
    
    # Create all tables
    db.create_all()
    
    # Import routes after models are defined
    import routes  # noqa: F401

    logger.info("Application initialized successfully")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
