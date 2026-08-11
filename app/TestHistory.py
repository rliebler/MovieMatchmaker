import os
from dotenv import load_dotenv
from GoogleSheets import get_user_history

# Load .env file
load_dotenv("../.env")

# Get spreadsheet ID
spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")

# For now, use the same user name you saved searches under
user = "Becca"

# Get history from Google Sheets
history = get_user_history(
    spreadsheet_id,
    user
)

print("\nSearch History:\n")

if len(history) == 0:
    print("No previous searches found.")

else:
    for search in history:

        print(f"Timestamp: {search['timestamp']}")
        print(
            f"Search: {search['actor']} - "
            f"{search['genre']} since {search['minimum_year']}"
        )

        print(f"1. {search['movie1']} - {search['rating1']}/10")
        print(f"2. {search['movie2']} - {search['rating2']}/10")
        print(f"3. {search['movie3']} - {search['rating3']}/10")

        print("-----------------------------")