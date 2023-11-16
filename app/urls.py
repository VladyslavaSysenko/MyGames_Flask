from flask import render_template, session, request
from controllers import *
from utils import login_required
from flask import Blueprint

bp = Blueprint("my_blueprint", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        return register_controller(request=request)
    else:
        return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in user"""

    # Forget any user_id
    session.clear()
    if request.method == "POST":
        return login_controller(request=request)
    else:
        return render_template("login.html")


@bp.route("/")
@login_required
def mygames():
    """Show user's games"""
    return my_games_controller()


@bp.route("/add", methods=["POST"])
@login_required
def add():
    """Add new game"""
    return add_game_controller(request=request)


# sort games
@bp.route("/sort", methods=["POST"])
@login_required
def sort():
    return sort_games_controller(request=request)


# delete a game
@bp.route("/delete", methods=["POST"])
def delete():
    return delete_game_controller(request=request)


# choose first player
@bp.route("/random")
def random():
    return render_template("random.html")


# search more games
@bp.route("/searchgames", methods=["GET", "POST"])
def search():
    return search_games_controller()


# add a site
@bp.route("/add_site", methods=["POST"])
@login_required
def add_site():
    return add_site_controller(request=request)


# delete a site
@bp.route("/delete_site", methods=["POST"])
def delete_site():
    return delete_site_controller(request=request)


# log user out
@bp.route("/logout")
def logout():
    return logout_controller()
