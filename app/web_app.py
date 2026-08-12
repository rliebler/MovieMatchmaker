from flask import Flask, render_template, request
from Genres import GENRES
from MainCode import get_movie_recommendations
from GoogleSheets import get_user_history
import os
from dotenv import load_dotenv

load_dotenv("../.env")

spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    error = None
    results = None

    actor = ""
    genre = ""
    minimum_year = ""

    if request.method == "POST":

        actor = request.form.get("actor", "").strip()
        genre = request.form.get("genre", "")
        minimum_year = request.form.get("minimum_year", "")

        if not actor:
            error = "Please enter an actor."

        elif not minimum_year:
            error = "Please enter an earliest release year."

        else:

            minimum_year = int(minimum_year)

            results, error = get_movie_recommendations(
                actor,
                genre,
                minimum_year
            )

    return render_template(
        "index.html",
        genres=GENRES.keys(),
        error=error,
        results=results,
        actor=actor,
        genre=genre,
        minimum_year=minimum_year
    )


# --------------------------------
# Search History Page
# --------------------------------

@app.route("/history")
def history():

    user = "DummyUser"  # Replace with actual user identification logic

    search_history = get_user_history(
        spreadsheet_id,
        user
    )

    return render_template(
        "history.html",
        history=search_history
    )


if __name__ == "__main__":
    app.run(debug=True)