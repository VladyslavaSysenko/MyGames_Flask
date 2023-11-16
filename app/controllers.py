from flask import redirect, render_template, session, request
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from models import User, Game, Site, DefaultSite
from app import db
from utils import apology


def register_controller(request=request):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Query database for username
    user = db.query(User).filter_by(username=request.form.get("username")).first()

    # Ensure username doesn't exist
    if user:
        return apology("username already exists", 400)

    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure confirmation password was submitted
    if not request.form.get("confirmation"):
        return apology("must provide password again", 400)

    # Ensure passwords match
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords do not match", 400)

    # Add new user to database
    new_user = User(
        username=request.form.get("username"),
        hash=generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=8
        ),
    )
    db.add(new_user)
    db.commit()

    # Remember which user has logged in
    session["user_id"] = new_user.id

    # Add default sites using SQLAlchemy syntax
    default_sites = db.query(DefaultSite).all()
    for default_site in default_sites:
        new_user_site = Site(id=new_user.id, name=default_site.name, url=default_site.url)
        db.add(new_user_site)
    db.commit()

    # Redirect user to home page
    return redirect("/")


def login_controller(request):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    # Query database for username
    user = db.query(User).filter_by(username=request.form.get("username")).first()

    # Ensure username exists and password is correct
    if not user or not check_password_hash(user.hash, request.form.get("password")):
        return apology("invalid username and/or password", 400)

    # Remember which user has logged in
    session["user_id"] = user.id

    # Redirect user to home page
    return redirect("/")


def my_games_controller():
    # Show games
    games = db.query(Game).filter_by(id=session["user_id"]).all()
    return render_template("mygames.html", games=games)


def add_game_controller(request):
    if request.form.get("date"):
        day = request.form.get("date")
    else:
        day = date.today()
    if request.form.get("price"):
        price = request.form.get("price")
    else:
        price = None
    # Insert game into database
    new_game = Game(
        id=session["user_id"],
        name=request.form.get("name"),
        review=request.form.get("review"),
        photo=request.form.get("photo"),
        own_it=True if request.form.get("own_it") == "yes" else False,
        rating=request.form.get("rating"),
        price=price,
        date=day,
    )
    db.add(new_game)
    db.commit()
    # Redirect user to list of his games
    return redirect("/")


def sort_games_controller(request):
    if request.form.get("sort_option_buy"):
        # Use SQLAlchemy query syntax for filtering by own_it
        games = (
            db.query(Game)
            .filter_by(id=session["user_id"], own_it=request.form.get("sort_option_buy"))
            .all()
        )
        sorted_names = {"yes": "Own it", "no": "Don't own it"}
        return render_template(
            "mygames.html",
            games=games,
            sort_name=sorted_names[request.form.get("sort_option_buy")],
            owning="yes",
        )
    else:
        # Use SQLAlchemy query syntax for ordering by the specified column
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

        # for sorted by button
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
    # Redirect user to list of his games
    return redirect("/searchgames")


def delete_site_controller(request):
    site_id = request.form.get("site_id")
    db.query(Site).filter_by(id=session["user_id"], site_id=site_id).delete()
    db.commit()
    return redirect("/searchgames")


def logout_controller():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")
