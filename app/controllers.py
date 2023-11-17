from flask import redirect, render_template, session, request
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from models import User, Game, Site, default_sites
from app import db
from utils import apology
from datetime import datetime


def register_controller(request=request):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400, "register")

    # Query database for username
    user = db.query(User).filter_by(username=request.form.get("username")).first()

    # Ensure username doesn't exist
    if user:
        return apology("username already exists", 400, "register")

    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide password", 400, "register")

    # Ensure confirmation password was submitted
    if not request.form.get("confirmation"):
        return apology("must provide password again", 400, "register")

    # Ensure passwords match
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords do not match", 400, "register")

    # Add new user to database
    new_user = User(
        username=request.form.get("username"),
        hash=generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=8
        ),
    )
    db.add(new_user)

    # Add default sites
    new_user.site.extend(default_sites)
    db.commit()

    # Remember which user has logged in
    session["user_id"] = new_user.id

    # Redirect user to home page
    return redirect("/")


def login_controller(request):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400, "login")

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 400, "login")

    # Query database for username
    user = db.query(User).filter_by(username=request.form.get("username")).first()

    # Ensure username exists and password is correct
    if not user or not check_password_hash(user.hash, request.form.get("password")):
        return apology("invalid username and/or password", 400, "login")

    # Remember which user has logged in
    session["user_id"] = user.id

    # Redirect user to home page
    return redirect("/")


def my_games_controller():
    # Show games
    games = db.query(Game).filter_by(id=session["user_id"]).all()
    return render_template("mygames.html", games=games)


def add_game_controller(request):
    # Add game
    day = request.form.get("date")
    price = request.form.get("price")
    # Insert game into database
    new_game = Game(
        id=session["user_id"],
        name=request.form.get("name"),
        review=request.form.get("review"),
        photo=request.form.get("photo"),
        own_it=True if request.form.get("own_it") == "True" else False,
        rating=request.form.get("rating"),
        price=price if price != "" else None,
        date=datetime.strptime(day, "%Y-%m-%d") if day != "" else date.today(),
    )
    db.add(new_game)
    db.commit()
    # Redirect user to list of his games
    return redirect("/")


def sort_games_controller(request):
    sort_buy = request.form.get("sort_option_buy")
    own_it = True if sort_buy == "True" else False
    # Get games filtering by own_it
    if sort_buy:
        games = db.query(Game).filter_by(id=session["user_id"], own_it=own_it).all()
        return render_template(
            "mygames.html",
            games=games,
            sort_name="Own it" if sort_buy else "Don't own it",
            owning="yes",
        )
    # Order by the specified column
    else:
        sort_option = request.form.get("sort_option")
        # Extract the column and order from the selected sort_option
        column, order = sort_option.rsplit("_", 1)
        if column == "name":
            games = (
                db.query(Game)
                .filter_by(id=session["user_id"])
                .order_by(
                    func.lower(Game.name).asc() if order == "asc" else func.lower(Game.name).desc()
                )
                .all()
            )
        # Basic cases where order by column
        else:
            games = (
                db.query(Game)
                .filter_by(id=session["user_id"])
                .order_by(
                    getattr(Game, column).asc() if order == "asc" else getattr(Game, column).desc()
                )
                .all()
            )

        # For sorted by button
        sorted_names = {
            "name_asc": "name, A-Z",
            "name_desc": "name, Z-A",
            "rating_asc": "rating, 0-10",
            "rating_desc": "rating, 10-0",
            "date_asc": "date, old to new",
            "date_desc": "date, new to old",
            "price_asc": "price, small to big",
            "price_desc": "price, big to small",
        }
        return render_template("mygames.html", games=games, sort_name=sorted_names[sort_option])


def delete_game_controller(request):
    game_id = request.form.get("game_id")
    db.query(Game).filter_by(id=session["user_id"], game_id=game_id).delete()
    db.commit()
    return redirect("/")


def search_games_controller():
    sites = db.query(Site).filter_by(id=session["user_id"]).all()
    return render_template("searchgames.html", sites=sites)


def add_site_controller(request):
    # Insert game into database
    new_site = Site(
        id=session["user_id"], name=request.form.get("name"), url=request.form.get("url")
    )
    db.add(new_site)
    db.commit()
    return redirect("/searchgames")


def delete_site_controller(request):
    # Delete site
    site_id = request.form.get("site_id")
    db.query(Site).filter_by(id=session["user_id"], site_id=site_id).delete()
    db.commit()
    return redirect("/searchgames")


def logout_controller():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")
