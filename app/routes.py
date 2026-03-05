import logging
from tabnanny import check

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
)
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from . import queue_worker
from .models import User, db

log = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index() -> str:
    return render_template("index.html")


@main.route("/login", methods=["POST", "GET"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Validate whether username and password were submitted or not
        if not username or not password:
            return render_template(
                "error.html", message="Must provide username and password"
            )

        # Query database for user
        user = User.query.filter_by(username=username).first()

        # Check whether user exists and password is correct
        if not user or not check_password_hash(user.password_hash, password):
            return render_template(
                "error.html", message="Invalid username and/or password"
            )

        return redirect("/")

    else:
        return render_template("login.html")


@main.route("/logout")
def logout():
    """Log user out."""
    session.clear()
    return redirect("/login")


@main.route("/register", methods=["POST", "GET"])
def register():
    """Register user."""
    if request.method == "POST":
        ...

    else:
        return render_template("register.html")


@main.route("/submit", methods=["POST", "GET"])
@login_required
def submit():
    if request.method == "POST":
        data = request.get_json()
        if not data or "code" not in data:
            return jsonify({"error": "No code received."}), 400

        code = data["code"]
        header = data.get("header", "")

        item = queue_worker.enqueue(code, header)
        return jsonify({"submission_id": item.submission_id})

    else:
        return render_template("submit.html")


@main.route("/status/<submission_id>")
def status(submission_id: str):
    result = queue_worker.get_status(submission_id)
    if result is None:
        return jsonify({"error": "Unknown submission ID."}), 404
    return jsonify(result)
