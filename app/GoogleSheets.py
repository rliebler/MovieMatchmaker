import os
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def get_sheets_service():

    private_key = os.getenv("GOOGLE_PRIVATE_KEY")

    # Environment variables sometimes store \n literally.
    # Convert them back into real line breaks.
    if private_key:
        private_key = private_key.replace("\\n", "\n")

    service_account_info = {
        "type": os.getenv("GOOGLE_TYPE"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI")
    }

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    return build(
        "sheets",
        "v4",
        credentials=credentials
    )


def save_search(
    spreadsheet_id,
    user,
    actor,
    genre,
    minimum_year,
    top_movies
):

    service = get_sheets_service()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        timestamp,
        user,
        actor,
        genre,
        minimum_year
    ]

    # Add the top 3 movies and ratings
    for movie in top_movies:
        row.append(movie["title"])
        row.append(round(movie["vote_average"], 2))

    body = {
        "values": [row]
    }

    # Add the row to the Google Sheet
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="History!A:K",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()


# --------------------------------
# Get user history
# --------------------------------

def get_user_history(spreadsheet_id, user):

    service = get_sheets_service()

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="History!A:K"
    ).execute()

    rows = result.get("values", [])

    history = []

    # Skip header row
    for row in rows[1:]:

        # Make sure the row has enough columns
        if len(row) >= 11:

            row_user = row[1]

            if row_user == user:

                history.append({
                    "timestamp": row[0],
                    "actor": row[2],
                    "genre": row[3],
                    "minimum_year": row[4],
                    "movie1": row[5],
                    "rating1": row[6],
                    "movie2": row[7],
                    "rating2": row[8],
                    "movie3": row[9],
                    "rating3": row[10]
                })

    # Show newest searches first
    history.reverse()

    return history