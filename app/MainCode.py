import os
import requests
from dotenv import load_dotenv
from Genres import GENRES

load_dotenv("../.env")

bearer_token = os.getenv("TMDB_BEARER_TOKEN")

# Create headers for TMDB API requests
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "accept": "application/json"
}
# --------------------------------
# Test API with an actor name and genre
# --------------------------------

actor = input("Enter an actor: ")
genre = input("Enter a genre: ").title()
minimum_year = int(input("Enter the earliest release year: "))

genre_id = GENRES.get(genre)


# --------------------------------
# Check genre
# --------------------------------

if genre_id is None:
    print("Genre not found.")
    exit()

else:

    # --------------------------------
    # Find actor
    # --------------------------------

    actor_url = "https://api.themoviedb.org/3/search/person"

    params = {
        "query": actor,
        "include_adult": False,
        "language": "en-US",
        "page": 1
    }

    response = requests.get(
        actor_url,
        headers=headers,
        params=params
    )

    actor_data = response.json()


    # --------------------------------
    # Check actor
    # --------------------------------

    if len(actor_data["results"]) == 0:
        print("Actor not found.")
        exit()

    else:

        actor_result = actor_data["results"][0]

        person_id = actor_result["id"]
        actor_name = actor_result["name"]

        print(f"\nFound actor: {actor_name}")


        # --------------------------------
        # Get actor movie credits
        # --------------------------------

        credits_url = (
            f"https://api.themoviedb.org/3/person/"
            f"{person_id}/movie_credits"
        )

        response = requests.get(
            credits_url,
            headers=headers
        )

        credits = response.json()


        # --------------------------------
        # Filter movies by genre
        # --------------------------------

        matching_movies = []

        for movie in credits["cast"]:

            release_date = movie.get("release_date", "")

            # Make sure the movie has a release date
            if release_date:
                release_year = int(release_date[:4])

                # Check genre AND minimum year
                if genre_id in movie["genre_ids"] and release_year >= minimum_year:
                    matching_movies.append(movie)

        # Sort highest rated to lowest rated
        matching_movies = sorted(
            matching_movies,
            key=lambda movie: movie.get("vote_average", 0),
            reverse=True
)
# Get only the top 3 movies
top_movies = matching_movies[:3]
other_movies = matching_movies[3:]


        # --------------------------------
        # Display results
        # --------------------------------

# --------------------------------
# Display top 3 results
# --------------------------------

print(f"\nTop 3 {genre} movies starring {actor_name} since {minimum_year}:\n")

if len(top_movies) == 0:
    print("No matching movies found.")

else:

    for index, movie in enumerate(top_movies, start=1):

        # Get movie information
        title = movie["title"]
        year = movie["release_date"][:4]
        synopsis = movie["overview"]
        rating = movie["vote_average"]
        movie_id = movie["id"]
        poster_path = movie.get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster_url = "No poster available"

        # Get cast for this movie
        cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

        response = requests.get(
            cast_url,
            headers=headers
        )

        cast_data = response.json()

        # Get first 3 billed actors
        top_cast = cast_data["cast"][:3]

        cast_names = []

        for actor in top_cast:
            cast_names.append(actor["name"])

        top_billing = ", ".join(cast_names)

        # DISPLAY EACH MOVIE
        print(f"\n{index}. {title}")
        print(f"    Release Year: {year}")
        print(f"    Synopsis: {synopsis}")
        print(f"    User Rating: {rating:.2f}/10")
        print(f"    Top Billing: {top_billing}")
        print(f"    Poster: {poster_url}")


# --------------------------------
# Display other matching movies
# --------------------------------

print(f"\nOther {genre} movies starring {actor_name} past {minimum_year}:\n")

if len(other_movies) == 0:
    print("No other matching movies found.")

else:
    for movie in other_movies:

        title = movie["title"]
        rating = movie["vote_average"]
        year = movie["release_date"][:4]

        print(f"{title} ({year}) - Rating: {rating:.2f}/10")