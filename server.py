"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db, User, Movie, Rating
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route("/movies")
def all_movies():
    """View all movies"""

    movies = crud.get_movies()
    # movies = Movie.all_movies()

    return render_template("all_movies.html", movies=movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)
    # movie = Movie.get_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    """View all users"""

    users = crud.get_users()
    # users = User.all_users()

    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    # user = User.get_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        # user = User.create(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)
    # user = User.get_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/login", methods=["POST"])
def login_process():
    """Process the user login"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    # user = User.get_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/update_rating", methods=["POST"])
def update_rating():
    """Updates rating for a movie."""
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]

    crud.update_rating(rating_id, updated_score)
    # Rating.update(rating_id, updated_score)
    db.session.commit()

    return "Success"

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Create a new rating for the movie."""

    # extracts the user_email from the user's session
    logged_in_email = session.get("user_email")
    # extracts rating_score from the form data 
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        # retrieves user object from db
        user = crud.get_user_by_email(logged_in_email)
        # user = User.get_by_email(logged_in_email)
        # retrieves movie object from db
        movie = crud.get_movie_by_id(movie_id)
        # movie = Movie.get_by_id(movie_id)

        # creates rating object using crud with the 2 previous objects we retrieved (user & movie)
        rating = crud.create_rating(user, movie, int(rating_score))
        # rating = Rating.create(user, movie, int(rating_score))
        # adds to the db
        db.session.add(rating)
        # saves to the db
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movies/{movie_id}")

# @app.route("/logout")
# def logout():
# """Log out."""
#     # del session['user_email']
#     session.clear()

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
