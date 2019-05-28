# Spotify-Invisibles
Make use of Spotify's Web API to access hidden data about your music and create top playlists for each category.

## About
Through their Web API, Spotify offers additional information on songs known as 'audio features'. Documentation on these features can be found
[here](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/). I chose to focus on the features that had values
over a range (danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, and valence), rather than those with
discrete values such as mode and key. The goal of this program was to select the top tracks in each category from the library of the user 
(myself) and create playlists for them. Unfortunately, the Spotify API makes it hard to access all saved tracks in the user's library, so 
instead this program evaluates all songs from all user playlists. I made use of the `Spotipy` library to help with the API Authorization Flow.

## To use
You will need a Spotify developer account, which can be created from the [dashboard](https://developer.spotify.com/dashboard/login), which
will provide you with a `CLIENT_ID` and a `CLIENT_SECRET`. You will also need your user ID, or `username`, which can be found in the link
that you use to share your Spotify profile (see [here](https://community.spotify.com/t5/Accounts/how-do-i-find-my-spotify-user-id/td-p/665532)). Define these variables in another file called spotifyLocalConfig.py.
Running the program will generate a prompt window where you give the application access to your account.

## Libraries used
- [Spotipy](https://spotipy.readthedocs.io/en/latest/)
- [Pandas](https://pandas.pydata.org/)
