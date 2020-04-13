# this is for heroku see 128 6:00

from app import app
from db import db
db.init_app(app)

@app.before_first_request
def create_tables():
  db.create_all()  # Create the db in the SQLALCHEMY_DATABASE_URI
