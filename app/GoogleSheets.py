import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheets_service():

    creds = None

    # Check if we've already logged into Google
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # If credentials don't exist or aren't valid
    if not creds or not creds.valid:

        # Refresh expired credentials
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Otherwise ask user to log into Google
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save login information for next time
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Connect to Google Sheets
    service = build(
        "sheets",
        "v4",
        credentials=creds
    )

    return service


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

# now to get user history
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