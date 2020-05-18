from sqlalchemy.testing.config import db
from sqlalchemy.dialects.mysql import JSON
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
def setup(app):
    app.config.from_object("config")
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Venue(db.Model):
    __tablename__ = "Venue"

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String)
    city                = db.Column(db.String(120))
    state               = db.Column(db.String(120))
    address             = db.Column(db.String(120))
    phone               = db.Column(db.String(120))
    genres              = db.Column(JSON)
    website             = db.Column(db.String(120))
    seeking_talent      = db.Column(db.String())
    seeking_description = db.Column(db.String())
    image_link          = db.Column(db.String(500))
    facebook_link       = db.Column(db.String(120))
    shows = db.relationship("Shows", backref="Venue", cascade="all,delete", lazy=True)


# TODO: implement any missing fields, as a database migration using Flask-Migrate  (DONE)
class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String)
    city        = db.Column(db.String(120))
    state       = db.Column(db.String(120))
    phone       = db.Column(db.String(120))
    genres      = db.Column(JSON)
    website     = db.Column(db.String(120))
    seeking_venue       = db.Column(db.String())
    seeking_description = db.Column(db.String())
    image_link          = db.Column(db.String(500))
    facebook_link       = db.Column(db.String(120))
    shows               = db.relationship("Shows", backref="Artist", cascade="all,delete", lazy=True)

# TODO: implement any missing fields, as a database migration using Flask-Migrate (DONE)
class Shows(db.Model):
    __tablename__ = "Shows"

    id          = db.Column(db.Integer, primary_key=True)
    artist_id   = db.Column(db.Integer, db.ForeignKey("Artist.id"))
    venue_id    = db.Column(db.Integer, db.ForeignKey("Venue.id"))
    start_time  = db.Column(db.DateTime)

