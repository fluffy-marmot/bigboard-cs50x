import logging

from flask import Blueprint, Response, jsonify, render_template, request

from . import queue_worker

log = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/")
def index() -> str:
    return render_template("index.html")


@main.route("/submit", methods=["POST", "GET"])
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
