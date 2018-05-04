from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Guest(db.Model):
    """Guests who have RSVP'd."""

    __tablename__ = "guests"
    guest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)


class Game(db.Model):
    """Board game."""

    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'))
    guest = db.relationship('Guest', backref='games')


def connect_to_db(app, db_uri="postgresql:///games"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""
    new_game = Game(name="Settlers of Catan", description="hellaaaaa long")

    db.session.add(new_game)
    db.session.commit()


if __name__ == '__main__':
    from party import app

    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
