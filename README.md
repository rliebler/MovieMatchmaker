# MovieMatchmaker
Final Project for Tech GB 2335

Movie Matchmaker Idea:

A user enters:

A favorite actor A preferred genre

Optionally, the oldest movie year they would consider

The application searches a movie API (we'll try the TMBD API I added below), returns the highest rated movies that fit the actor and genre, along with a description of the movie and the movie poster, and records the results in Google Sheets.

Display this in a web browser format.

How it would work from user perspective: Log into the app with Google Login Type in: Favorite Actor: Genre(s): Oldest Release Year Acceptable:

Then Movie Matchmaker looks at all the movies the actor is in, genre, year the movie was released, and the critic ratings and returns the top three options.

Must Display:

Movie Title
Release Year
Synopsis
Critic Rating
Top Billing
Movie Poster
At the bottom of the search there should be an option to do another search. If possible, the search bar should save the previous searched actor, genre, and oldest release year acceptable in case the user just wants to modify their search rather than start fresh.

Then will be a "Clear" option so they can start fresh if they don't want to modify.

Then on a second tab on the application we want the user to be able to see previous search history they have. We'll have a tab called "Recent Searches" and we can see the returned results which are stored in Google Sheets.

Error Handling Considerations:

Message to display if TMBD API is down, "We're sorry, we're experiencing some difficulties connecting. Please try again later."
If for a criteria 2 or less results are returned:
"X results match your search criteria for [ACTOR_NAME], [GENRE], and [XXXX] Release Year Minimum. Please refine your search for better results."
Message if connection to google sheets for search history is failing, "We're sorry, we're experiencing some difficulties connecting. Please try again later."

Things to consider from this API:

returns genre code not genre name so will need to match up the code with the genre to display back to the user
Slightly concerned it only returned a few Matt Damon movies not his whole database so hopefully it can return all his movies so then we can sort and do scoring based on genre, release year, and rating Tested this part out now it gives me all movies no longer a concern
rating metric: vote_average
Attributes from the response we'll need to map:

title
release_date
overview - this will be the move synopsis
genre_ids - will need to match IDs with genre names
poster_path - display the movie post image
vote_average - viewer rating score out of 10.