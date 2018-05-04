"""Flask site for Balloonicorn's Party."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import Game, connect_to_db, db, Guest

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    new_guest = Guest(name=name, email=email)
    db.session.add(new_guest)
    db.session.commit()

    session['RSVP'] = True
    session['email'] = email
    flash("Yay!")

    return redirect("/")


@app.route("/guests")
def guests():
    """View guest list."""

    guests = Guest.query.all()

    return render_template("guests.html", guests=guests)


@app.route("/games")
def games():
    games = Game.query.all()

    try:
        if session['RSVP']:
            return render_template("games.html", games=games)

    except:
        return redirect("/")


@app.route("/game-confirmation", methods=['POST'])
def confirm_game():
    game = request.form.get("game_name")
    description = request.form.get("description")
    guest_id = Guest.query.filter_by(email=session['email']).one()

    if Game.query.filter_by(name=game).all():
        flash("Someone's already bringing that game!")

        return redirect("/games")

    else:
        user_game = Game(name=game, description=description, guest_id=guest_id)
        db.session.add(user_game)
        db.session.commit()

        return render_template("game-confirmation.html", user_game=user_game)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()
