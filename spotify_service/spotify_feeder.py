import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


def setup():
    # Function to create spotify agent that will be used to access spotify database via spotipy APIs
    # @params: None
    # @returns: spotify_agent that is created by Spotify

    ### Please fill these environment variables in system controls, or uncomment and change the source code here ###
    # os.environ['SPOTIPY_CLIENT_ID'] = ''
    # os.environ['SPOTIPY_CLIENT_SECRET'] = ''
    # os.environ['SPOTIPY_REDIRECT_URI'] = ''

    auth_manager = SpotifyOAuth(scope="playlist-modify-public")
    spotify_agent = spotipy.Spotify(auth_manager=auth_manager)
    return spotify_agent

def create_required_playlist(spotify_agent, username):
    # Search for "From Gaana" public playlist. Create if not found.
    # @params: Spotify_agent created by Spotipy
    # @returns: "From Gaana" public playlist ID
    playlists = spotify_agent.user_playlists(username)
    playlist_found=False
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if playlist['name'] == "From Gaana":
                required_playlist_id = playlist['id']
                return required_playlist_id
        if playlists['next']:
            playlists = spotify_agent.next(playlists)
        else:
            playlists = None

    if not playlist_found:
        spotify_agent.user_playlist_create(username, 'From Gaana', public=True, description= "Music added from Gaana playlist")

        # Retrieve the playlist data again, since the new playlist could be anywhere in the list
        # ( I can't assume that it'll always be the first, although it does look like that way).
        playlists = spotify_agent.user_playlists(username)
        playlist_found = False
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                if playlist['name'] == "From Gaana":
                    required_playlist_id = playlist['id']
                    return required_playlist_id
            if playlists['next']:
                playlists = spotify_agent.next(playlists)
            else:
                playlists = None
        if not playlist_found:
            # Ideally we should always find the playlist after adding it.
            # So this condition should never be true
            print("ERROR: From Gaana playlist couldn't be retrieved even after inception. Exiting.")
            exit(5)


def spotify_push(songs):
    # Driver function that sets up Spotify agent via Spotipy, creates a playlist if uncreated and pushes songs into it.
    # @params songs: list of Song type objects.
    # @returns completion code: 0 for SUCCESS, 1 for ERROR

    # Setup Spotipy API for authentication
    print("Setting up Spotify Client")
    spotify_agent = setup()

    # Ask for username to create public playlist
    print("Enter your username: ")
    username = input()

    # Create "From Gaana" playlist if doesn't already exist.
    new_playlist_id = create_required_playlist(spotify_agent, username)

    # Fetch track IDs in spotify database
    track_ids = []
    successfully_ported = []
    failed_to_port = []
    print("Printing list of matched songs")
    for i in range(len(songs)):
        song = songs[i]
        title = song.get_title()
        artists_list = song.get_artists()
        artists = " ".join(artists_list)
        searched_track = spotify_agent.search(title + ' ' + artists, type='track')
        number_of_items_found = searched_track['tracks']['total']
        if number_of_items_found == 0:  # No match found for that song
            print("No match for Gaana's song: {} by {}".format(title, ", ".join(artists_list)))
            failed_to_port.append("{} by {}".format(title, ", ".join(artists_list)))
            continue

        # Find artists in spotify's matched track
        searched_artists_name = []
        for artists_index in range(len(searched_track['tracks']['items'][0]['artists'])):
            searched_artists_name.append(searched_track['tracks']['items'][0]['artists'][artists_index]['name'])

        # Display to user
        display_result = searched_track['tracks']['items'][0]['name']+" By "+", ".join(searched_artists_name)
        print(display_result)
        successfully_ported.append(display_result)

        # Store Track IDs
        track_ids.append(searched_track['tracks']['items'][0]['id'])

    print("\nProceeding to add songs...")
    # Add songs in bulk of 100s because that is the upper limit of Spotify API
    number_of_iterations_needed = len(track_ids)//100
    for i in range(number_of_iterations_needed):
        spotify_agent.playlist_add_items(new_playlist_id, track_ids[i*100 : (i+1)*100])
    spotify_agent.playlist_add_items(new_playlist_id, track_ids[number_of_iterations_needed*100:])

    return successfully_ported, failed_to_port






