# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *  
import string

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database (DONE)
SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@localhost:5432/postgres"

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "Venue"

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String)
    city                = db.Column(db.String(120))
    state               = db.Column(db.String(120))
    address             = db.Column(db.String(120))
    phone               = db.Column(db.String(120))
    genres              = db.Column(ARRAY(db.String(120)))
    website             = db.Column(db.String(120))
    seeking_talent      = db.Column(db.String())
    seeking_description = db.Column(db.String())
    image_link          = db.Column(db.String(500))
    facebook_link       = db.Column(db.String(120))
    shows = db.relationship("Shows", backref="Venue", lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate  (DONE)


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String)
    city        = db.Column(db.String(120))
    state       = db.Column(db.String(120))
    phone       = db.Column(db.String(120))
    genres      = db.Column(db.String(120))
    website     = db.Column(db.String(120))
    seeking_venue       = db.Column(db.String())
    seeking_description = db.Column(db.String())
    image_link          = db.Column(db.String(500))
    facebook_link       = db.Column(db.String(120))
    shows               = db.relationship("Shows", backref="Artist", lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate (DONE)


class Shows(db.Model):
    __tablename__ = "Shows"

    id          = db.Column(db.Integer, primary_key=True)
    artist_id   = db.Column(db.Integer, db.ForeignKey("Artist.id"))
    venue_id    = db.Column(db.Integer, db.ForeignKey("Venue.id"))
    start_time  = db.Column(db.String(25))


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data. (DONE)
    #       num_shows should be aggregated based on number of upcoming shows per venue.
  
    venues = Venue.query.group_by(Venue.id, Venue.city, Venue.state).all()
    data = []

    for venue in venues :
        data.append({
            "city": venue.city,
            "state":venue.state,
            "venues":[{
                "id": venue.id,
                "name": venue.name
            }]
        })

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop". (DONE)
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee" (DONE)
    response = request.form.get('search_term', '')
    response = response.lower()

    venues = db.session.query(Venue).filter(Venue.name.ilike('%' + response + '%')).all()
    results = []
    
    for v in venues:
        print(v.name)
        results.append({
                'id': v.id,
                'name' : v.name
        })

    response={
        "count": len(results),
        "data": results
    }

    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    
    # shows the venue page with the given venue_id
    result = db.session.query(Venue).filter(Venue.id == venue_id)
    result = result[0]

    # TODO: replace with real venue data from the venues table, using venue_id (DONE)

    resdata = {
        "id": result.id,
        "name": result.name,
        "genres": result.genres,
        "address": result.address,
        "city": result.city,
        "state": result.state,
        "phone": result.phone,
        "website": result.website,
        "facebook_link": result.facebook_link,
        "seeking_talent": result.seeking_talent,
        "seeking_description": result.seeking_description,
        "image_link": result.image_link,
        "past_shows": [
            {
                "artist_id": 4,
                "artist_name": "Guns N Petals",
                "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
                "start_time": "2019-05-21T21:30:00.000Z",
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    
    data = list(filter(lambda d: d["id"] == venue_id, [resdata]))[0]
    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead (DONE)
    # TODO: modify data to be the data object returned from db insertion

    try:
        name            = request.form.get("name")
        city            = request.form.get("city")
        state           = request.form.get("state")
        address         = request.form.get("address")
        phone           = request.form.get("phone")
        imageLink       = request.form.get("image_link")
        genres          = request.form.get("genres")
        facebookLink    = request.form.get("facebook_link")
        website         = request.form.get("website")
        seeking_talent    = request.form.get("facebook_link")
        seeking_description    = request.form.get("facebook_link")

        venue_to_add = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            image_link=imageLink,
            genres=genres,
            facebook_link=facebookLink,
            website=website,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description
        )

        db.session.add(venue_to_add)
        db.session.commit()

        # on successful db insert, flash success
        flash("Venue " + request.form["name"] + " was successfully listed!")

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    except:
        flash("An error occurred. Venue " + name + " could not be listed.")
        db.session.rollback()
    finally:
        db.session.close()
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using (DONE)
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    try:
        print('DELETING VENUE NUMBER: ' + venue_id)
        result = db.session.query(Venue).filter(Venue.id==venue_id).delete()
        db.session.commit()
    except:
            flash("An error occurred. Venue " + result.name + " could not be deleted.")
            db.session.rollback()
    finally:
            db.session.close()
    
    return redirect(url_for('index'))

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    


#  Artists
#  ----------------------------------------------------------------


@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database (DONE)
    artists = Artist.query.group_by(Artist.id, Artist.name).all()

    data = []

    for a in artists :
        data.append({
            'id' : a.id,
            'name' : a.name
        })

    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. (DONE)

    response = request.form.get('search_term', '')
    response = response.lower()

    artists = db.session.query(Artist).filter(Artist.name.ilike('%' + response + '%')).all()
    results = []
    
    for a in artists:
        print(a.name)
        results.append({
                'id': a.id,
                'name' : a.name
        })

    response={
        "count": len(results),
        "data": results
    }

    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):

    result = db.session.query(Artist).filter(Artist.id == artist_id)
    result = result[0]

    resdata = {
        "id": result.id,
        "name": result.name,
        "genres": result.genres,
        "city": result.city,
        "state": result.state,
        "phone": result.phone,
        "website": result.website,
        "facebook_link": result.facebook_link,
        "seeking_venue": result.seeking_venue,
        "seeking_description": result.seeking_description,
        "image_link": result.image_link,
        "past_shows": [
            {
                "venue_id": 1,
                "venue_name": "The Musical Hop",
                "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
                "start_time": "2019-05-21T21:30:00.000Z",
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }

    data = list(filter(lambda d: d["id"] == artist_id, [resdata]))[0]
    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------


@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):

    result = db.session.query(Artist).filter(Artist.id == artist_id)
    result = result[0]
    artist = result
    form = ArtistForm(obj=artist)

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    
    result = db.session.query(Artist).filter(Artist.id == artist_id)
    result = result[0]
    artist = result

    name            = request.form.get('name')
    city            = request.form.get('city')
    state           = request.form.get('state')
    phone           = request.form.get('phone')
    genres          = request.form.get('genres')
    imageLink       = request.form.get('image link')
    facebookLink    = request.form.get('facebook_link')
    website         = request.form.get('website')
    seeking_venue   = request.form.get('seeking_venue')
    seeking_description = request.form.get('seeking_description')

    artist.name = name
    artist.city = city
    artist.state = state
    artist.phone = phone
    artist.genres = genres
    artist.image_link = imageLink
    artist.facebook_link = facebookLink
    artist.website = website
    artist.seeking_venue = seeking_venue
    artist.seeking_description = seeking_description

    db.session.commit()
    db.session.close()

    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    
    result = db.session.query(Venue).filter(Venue.id == venue_id)
    result = result[0]
    venue = result
    form = VenueForm(obj=venue)
    
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing

    result = db.session.query(Venue).filter(Venue.id == venue_id)
    result = result[0]
    venue = result

    name            = request.form.get('name')
    city            = request.form.get('city')
    state           = request.form.get('state')
    phone           = request.form.get('phone')
    genres          = request.form.get('genres')
    imageLink       = request.form.get('image link')
    facebookLink    = request.form.get('facebook_link')
    website         = request.form.get('website')
    seeking_talent   = request.form.get('seeking_talent')
    seeking_description = request.form.get('seeking_description')


    venue.name = name
    venue.city = city
    venue.state = state
    venue.phone = phone
    venue.genres = genres
    venue.image_link = imageLink
    venue.facebook_link = facebookLink
    venue.website = website
    venue.seeking_talent = seeking_talent
    venue.seeking_description = seeking_description

    db.session.commit()
    db.session.close()

    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    try:
        name                = request.form.get("name")
        city                = request.form.get("city")
        state               = request.form.get("state")
        phone               = request.form.get("phone")
        imageLink           = request.form.get("image_link")
        genres              = request.form.get("genres")
        facebookLink        = request.form.get("facebook_link")
        website             = request.form.get("website")
        seeking_venue       = request.form.get("seeking_venue")
        seeking_description = request.form.get("seeking_description")
        
        artist_to_add = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            image_link=imageLink,
            genres=genres,
            facebook_link=facebookLink,
            website=website,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
        )

        db.session.add(artist_to_add)
        db.session.commit()

        # on successful db insert, flash success
        flash("Artist " + request.form["name"] + " was successfully listed!")

    except:
        flash("An error occurred. Artist " + name + " could not be listed.")
        db.session.rollback()
    finally:
        db.session.close()

    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows

    shows = Shows.query.group_by(Shows.id, Venue.city, Venue.state).all()
    venue = Venue.query.group_by(Venue.id, Venue.city, Venue.state).all()
    artist = Artist.query.group_by(Artist.id, Artist.name).all()

    artist_id
    venue_id
    artist_name
    venue_name
    artist_image_link
    start_time|datetime('full')


    data = []

    for venue in venues :
        data.append({
            "city": venue.city,
            "state":venue.state,
            "venues":[{
                "id": venue.id,
                "name": venue.name
            }]
        })

    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [
        {
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z",
        },
    ]
    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form 
    # TODO: insert form data as a new Show record in the db, instead (DONE)

    err = False
    try:

        date_format = '%Y-%m-%d %H:%M:%S'
        show = Shows()
        show.artist_id = request.form['artist_id']
        show.venue_id = request.form['venue_id']
        show.start_time = datetime.strptime(request.form['start_time'], date_format)
        db.session.add(show)
        db.session.commit()


    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except:
        err = True
        db.session.rollback()
    finally:
        db.session.close()
        if err: flash('ERROR. The entered show has not been listed.')
        else: flash('Show was successfully listed!')

    # on successful db insert, flash success

    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run(debug=True)

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
